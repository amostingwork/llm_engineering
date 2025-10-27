from openai import OpenAI
import json
from typing import Dict, List, Any, Optional
from config_manager import Config

"""
Given a dict of posts from multiple blogs, filter and score them using OpenAI.

Args:
    posts: Mapping of blog_name -> list of post dictionaries
    system_prompt: Context prompt (defines assistant persona)
    user_prompt: Description of user's interests
    config: Configuration object containing API and filtering settings

Returns:
    A list of relevant article dicts:
    [
        {"title": "...", "reason_and_summary": "...", "link": "...", "relevance_score": 8.3},
        ...
    ]
"""
def filter_relevant_articles(
    posts: Dict[str, List[Dict[str, Any]]],
    system_prompt: str,
    user_prompt: str,
    config: Optional[Config] = None
) -> List[Dict[str, Any]]:
    
    # Initialize OpenAI client with configuration
    if config:
        client = OpenAI(
            base_url=config.api.ollama_base_url, 
            api_key=config.api.ollama_api_key
        )
        model_name = config.api.model_name
        temperature = config.api.temperature
        relevance_threshold = config.filtering.relevance_threshold
        max_articles = config.filtering.max_articles_to_process
    else:
        # Fallback to default values
        client = OpenAI(base_url="http://localhost:11434/v1", api_key='ollama')
        model_name = "llama3.2"
        temperature = 0.2
        relevance_threshold = 6.0
        max_articles = 100

    # Step 1: Flatten all posts into a single list
    all_summaries = []
    for blog_name, entries in posts.items():
        for entry in entries:
            all_summaries.append({
                "source": blog_name,
                "title": entry["title"],
                "summary": entry["summary"],
                "link": entry["link"]
            })

    # Limit articles to process based on configuration
    if len(all_summaries) > max_articles:
        print(f"Limiting articles to process from {len(all_summaries)} to {max_articles}")
        all_summaries = all_summaries[:max_articles]

    # Step 2: Build model input
    article_list_text = "\n\n".join(
        [f"Title: {a['title']}\nSummary: {a['summary']}\nLink: {a['link']}" for a in all_summaries]
    )

    full_prompt = (
        f"{user_prompt}\n\n"
        "Here is a list of articles with summaries:\n\n"
        f"{article_list_text}\n\n"
        "Return only a JSON object in this format:\n"
        "{\n"
        '  "relevant_articles": [\n'
        '    {"title": "...", "article_summary": "...", "link": "...", "relevance_score": 0.0, "reason_for_relevance_score": "..."}\n'
        "  ]\n"
        "}\n"
        f"Include the title of the article, summary of the article, the link, the relevance score you give to the article and the reason why you gave the relevance score in the JSON object.\n"
        f"Only include articles with relevance_score >= {relevance_threshold}.\n"
        "Use 1 decimal place for the score.\n"
        "I want you to follow the above instructions exactly, do not deviate.\n"
    )

    # Step 3: Call the model
    print("Calling LLM...")
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            temperature=temperature
        )

        raw_output = response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error calling LLM: {e}")
        return []

    # Step 4: Parse JSON safely
    try:
        result = json.loads(raw_output)
        relevant_articles = result.get("relevant_articles", [])
        print(f"Successfully parsed {len(relevant_articles)} relevant articles")
    except json.JSONDecodeError as e:
        print(f"Model returned invalid JSON: {e}")
        print("⚠️ Warning: Model returned invalid JSON. Output:")
        print(raw_output)
        relevant_articles = []

    # Step 5: Apply deduplication if enabled
    if config and config.filtering.enable_deduplication:
        relevant_articles = _deduplicate_articles(relevant_articles, config.filtering.deduplication_threshold)
        print(f"After deduplication: {len(relevant_articles)} articles")

    return relevant_articles

def _deduplicate_articles(articles: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]:
    """
    Remove duplicate articles based on title similarity.
    
    Args:
        articles: List of article dictionaries
        threshold: Similarity threshold (0-1) for considering articles as duplicates
        
    Returns:
        List of deduplicated articles
    """
    if not articles:
        return articles
    
    # Simple deduplication based on title similarity
    # In a more sophisticated implementation, you could use text similarity algorithms
    seen_titles = set()
    deduplicated = []
    
    for article in articles:
        title = article.get('title', '').lower().strip()
        
        # Check if we've seen a similar title
        is_duplicate = False
        for seen_title in seen_titles:
            # Simple similarity check - you could use more sophisticated algorithms
            if _calculate_similarity(title, seen_title) > threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            seen_titles.add(title)
            deduplicated.append(article)
    
    return deduplicated

def _calculate_similarity(title1: str, title2: str) -> float:
    """
    Calculate simple similarity between two titles.
    This is a basic implementation - you could use more sophisticated algorithms.
    """
    # Simple word overlap similarity
    words1 = set(title1.split())
    words2 = set(title2.split())
    
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0
