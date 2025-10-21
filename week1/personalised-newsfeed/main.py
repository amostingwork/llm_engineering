import scraper # scraper.py
import filter # filter.py

def main():
    all_posts = scraper.fetch_all_feeds("week1/personalised-newsfeed/tech_blogs.json")

    PER_BLOG_LIMIT = 3  # Adjust this number as needed
    for blog_name in all_posts:
        all_posts[blog_name] = all_posts[blog_name][:PER_BLOG_LIMIT]

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
    
    # Prompts for filtering
    system_prompt = """
        You are my personal assistant who knows that I am very interested in catching up with the latest tech news.
        Return only valid JSON exactly in the requested schema.
    """

    user_prompt = """
        I am a junior software engineer who is very interested in keeping up with the latest tech trends and also learn new skills that I do not have.
        My company currently requires me to code in C# for backend and Typescript for frontend.
        I am interested in the latest AI developments, system design, software design and software development life cycle. 
        Help me to sieve through the websites that I have provided and give me a summary of the learnings from these articles. 
    """
    print("Getting relevant articles...")
    # Get relevant articles
    relevant_articles = filter.filter_relevant_articles(
        posts=all_posts,
        system_prompt=system_prompt,
        user_prompt=user_prompt
    ) 

    print("\n🧭 Relevant Articles")
    print("=" * 80)
    for a in relevant_articles:
        print(f"- [{a.get('title','Untitled')}]({a.get('link','')}) — score: {a.get('relevance_score','?')}")

if __name__ == "__main__":
    main()