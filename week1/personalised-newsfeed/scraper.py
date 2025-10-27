import feedparser
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from config_manager import Config

"""
Load tech blog URLs from configuration.

Args:
    config: Configuration object containing tech blogs
    
Returns:
    Dictionary mapping blog names to RSS feed URLs
"""
def load_tech_blogs(config: Config) -> Dict[str, str]:
    try:
        blogs = config.tech_blogs.blogs
        print(f"✅ Loaded {len(blogs)} tech blogs from configuration")
        return blogs
    except Exception as e:
        print(f"❌ Error loading tech blogs from config: {e}")
        return {}

"""
Fetch posts from all tech blogs in the configuration.

Args:
    config: Configuration object containing scraping settings and tech blogs
    
Returns:
    Dictionary mapping blog names to lists of posts
"""
def fetch_all_feeds(config: Config) -> Dict[str, List[Dict[str, Any]]]:
    blogs = load_tech_blogs(config)
    all_posts = {}
    
    for blog_name, feed_url in blogs.items():
        print(f"\n📰 Fetching posts from {blog_name}...")
        
        # Retry logic based on configuration
        retry_attempts = config.scraping.retry_attempts
        retry_delay = config.scraping.retry_delay
        
        for attempt in range(retry_attempts):
            try:
                posts = fetch_feed(feed_url, config)
                all_posts[blog_name] = posts
                break
            except Exception as e:
                if attempt < retry_attempts - 1:
                    print(f"⚠️ Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"❌ Error fetching {blog_name}: {e}")
                    all_posts[blog_name] = []
    
    return all_posts

"""
Fetches and parses the RSS feed from the given URL.

Args:
    url: RSS feed URL
    config: Configuration object containing scraping settings

Returns:
    A list of dictionaries, each representing one post.
"""
def fetch_feed(url: str, config: Optional[Config] = None) -> List[Dict[str, Any]]:
    print(f"Fetching feed from: {url}")
    
    try:
        feed = feedparser.parse(url)

        if feed.bozo:  # bozo == True means a parsing error occurred
            print(f"⚠️ Warning: Feed parsing error: {feed.bozo_exception}")

        posts = []
        for entry in feed.entries:
            # Extract relevant fields
            post = {
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published", None),
                "summary": entry.get("summary", None),
                # Optionally extract other metadata if available
                "author": entry.get("author", None),
                "tags": [t["term"] for t in entry.get("tags", [])] if "tags" in entry else [],
            }
            posts.append(post)

        print(f"✅ Retrieved {len(posts)} posts.")
        return posts
        
    except Exception as e:
        print(f"❌ Error fetching feed from {url}: {e}")
        raise

"""
Converts a feed 'published' date string into a datetime object.
"""
def normalize_date(date_str: str) -> datetime:
    try:
        return datetime(*feedparser.parse(date_str).updated_parsed[:6])
    except Exception:
        return None

"""
Entry point for testing the scraper.
"""
def main():
    from config_manager import get_config
    
    config = get_config()
    posts = fetch_all_feeds(config)

    # Display results
    total_posts = sum(len(posts) for posts in posts.values())
    print(f"\n📊 Summary: Retrieved {total_posts} total posts from {len(posts)} blogs")
    
    # Show latest posts from each blog
    for blog_name, posts in posts.items():
        print(f"\n🔗 {blog_name} ({len(posts)} posts)")
        print("-" * 50)
        
        # Show latest 3 posts from each blog
        for i, post in enumerate(posts[:3]):
            print(f"\n[{i+1}] {post['title']}")
            print(f"URL: {post['link']}")
            print(f"Published: {post['published']}")
            print(f"Summary snippet: {post['summary'][:150]}...")
            print(f"Tags: {post['tags']}")


if __name__ == "__main__":
    main()
