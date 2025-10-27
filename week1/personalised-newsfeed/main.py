import scraper # scraper.py
import filter # filter.py
import display_data # display_data.py
from config_manager import config_manager, get_config

def main():
    # Load configuration
    config = get_config()
    
    print("Starting personalised newsfeed application")
    
    # Fetch posts from tech blogs using configuration
    all_posts = scraper.fetch_all_feeds(config)

    # Apply per-blog limit from configuration
    per_blog_limit = config.scraping.per_blog_limit
    for blog_name in all_posts:
        all_posts[blog_name] = all_posts[blog_name][:per_blog_limit]

    # Display results
    total_posts = sum(len(posts) for posts in all_posts.values())
    print(f"\n📊 Summary: Retrieved {total_posts} total posts from {len(all_posts)} blogs")
    
    # Show latest posts from each blog
    for blog_name, posts in all_posts.items():
        print(f"\n🔗 {blog_name} ({len(posts)} posts)")
        print("-" * 50)
        
        # Show latest 3 posts from each blog
        for i, post in enumerate(posts[:3]):
            print(f"\n[{i+1}] {post['title']}")
            print(f"URL: {post['link']}")
            print(f"Published: {post['published']}")
            print(f"Summary snippet: {post['summary'][:150]}...")
            print(f"Tags: {post['tags']}")
    
    # Get prompts from configuration
    system_prompt = config.prompts.system_prompt
    user_prompt = config.prompts.user_prompt
    
    print("Getting relevant articles...")
    
    # Get relevant articles
    relevant_articles = filter.filter_relevant_articles(
        posts=all_posts,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        config=config
    ) 

    # Create output directory if it doesn't exist
    output_dir = config.output.output_directory
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output file path
    output_filename = os.path.join(output_dir, config.output.markdown_filename)
    
    # After getting relevant_articles
    markdown_file = display_data.create_markdown_file(relevant_articles, output_filename, config)
    display_data.display_articles_summary(relevant_articles, config)
    
    print(f"Application completed successfully. Generated {len(relevant_articles)} relevant articles.")

if __name__ == "__main__":
    main()