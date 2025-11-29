# blog_app/services/utils_law.py

from ..core.llm import get_llm_model
from ..prompts import prompts_law
import json
from typing import List 

llm = get_llm_model()

def _extract_json_array(text: str) -> List[str]:
    """
    A robust function to extract a JSON array from a string.
    """
    try:
        start_index = text.find('[')
        end_index = text.rfind(']')
        
        if start_index != -1 and end_index != -1 and end_index > start_index:
            json_str = text[start_index : end_index + 1]
            return json.loads(json_str)
        else:
            return json.loads(text.strip())
    except json.JSONDecodeError:
        print(f"DEBUG: Failed to decode JSON from AI response: {text}")
        return []

async def is_topic_indian_law(topic: str) -> bool:
    messages = prompts_law.IS_INDIAN_LAW_PROMPT.format_messages(topic=topic)
    try:
        response = await llm.ainvoke(messages)
        content_str = str(response.content) 
        return "yes" in content_str.strip().lower()
    except Exception as e:
        print(f"DEBUG: AI call failed in is_topic_indian_law: {e}")
        return True

async def get_latest_law_news_topics() -> List[str]:
    messages = prompts_law.LATEST_INDIAN_LAW_NEWS_PROMPT.format_messages()
    try:
        response = await llm.ainvoke(messages)
        content_str = str(response.content)
        return _extract_json_array(content_str)
    except Exception as e:
        print(f"DEBUG: AI call failed in get_latest_law_news_topics: {e}")
        return []

async def get_related_blog_ideas(topic: str, count: int, existing_titles: List[str]) -> List[str]:
    messages = prompts_law.RELATED_BLOG_IDEAS_PROMPT.format_messages(
        topic=topic, count=count, existing_titles=existing_titles
    )
    try:
        response = await llm.ainvoke(messages)
        content_str = str(response.content)
        return _extract_json_array(content_str)
    except Exception as e:
        print(f"DEBUG: AI call failed in get_related_blog_ideas: {e}")
        return []

async def generate_law_blog_from_title(title: str) -> str:
    """Generates the full text content of a blog from its title using an async AI call."""
    messages = prompts_law.LAW_BLOG_GENERATION_PROMPT.format_messages(title=title)
    try:
        response = await llm.ainvoke(messages)
        # FIX: Ensure content is a string before calling .strip()
        return str(response.content).strip()
    except Exception as e:
        print(f"DEBUG: AI call failed in generate_law_blog_from_title: {e}")
        return f"Error: Could not generate blog content due to an API error. Details: {e}"