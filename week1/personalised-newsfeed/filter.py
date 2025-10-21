from openai import OpenAI
import json
from typing import Dict, List, Any

OLLAMA_BASE_URL = "http://localhost:11434/v1"

client = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')

"""
Given a dict of posts from multiple blogs, filter and score them using OpenAI.

Args:
    posts: Mapping of blog_name -> list of post dictionaries
    system_prompt: Context prompt (defines assistant persona)
    user_prompt: Description of user's interests

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
    user_prompt: str
) -> List[Dict[str, Any]]:

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
        '    {"title": "...", "reason_and_summary": "...", "link": "...", "relevance_score": 0.0}\n'
        "  ]\n"
        "}\n"
        "Only include articles with relevance_score >= 6.0.\n"
        "Use 1 decimal place for the score.\n"
    )

    # Step 3: Call the model
    print("Calling LLM...")
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.2
    )

    raw_output = response.choices[0].message.content.strip()

    # Step 4: Parse JSON safely
    try:
        result = json.loads(raw_output)
        relevant_articles = result.get("relevant_articles", [])
    except json.JSONDecodeError:
        print("⚠️ Warning: Model returned invalid JSON. Output:")
        print(raw_output)
        relevant_articles = []

    return relevant_articles
