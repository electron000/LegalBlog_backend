# blog_app/prompts/prompts_law.py

from langchain.prompts import ChatPromptTemplate

# Prompt 1: To classify if a topic is related to Indian Law
IS_INDIAN_LAW_PROMPT = ChatPromptTemplate.from_template(
    """
    Analyze the following topic. Is it related to the Indian legal system, Indian legislation, courts in India, or specific Indian acts?
    Answer with only a single word: 'Yes' or 'No'.

    Topic: "{topic}"
    """
)

# --- MODIFIED PROMPT ---
LATEST_INDIAN_LAW_NEWS_PROMPT = ChatPromptTemplate.from_template(
    """
    You are a legal news aggregator for India. 
    List the top 6 most recent and significant topics or news headlines in Indian law. 
    
    IMPORTANT: Provide the output ONLY as a valid JSON array of strings. Do not include any other text, explanation, or markdown formatting. Your response must start with '[' and end with ']'.

    Example format:
    ["Title of News 1", "Title of News 2", "Title of News 3", "Title of News 4", "Title of News 5", "Title of News 6"]
    """
)


# Prompt 3: To generate unique, related blog titles from a user's topic
RELATED_BLOG_IDEAS_PROMPT = ChatPromptTemplate.from_template(
    """
    You are a legal content strategist. Based on the user's main topic, generate {count} unique and engaging blog post titles that are related but distinct.
    Do not include any of the titles from the 'existing_titles' list.

    Main Topic: "{topic}"
    Existing Titles to Exclude: {existing_titles}
    
    IMPORTANT: Provide the output ONLY as a valid JSON array of strings. Do not include any other text, explanation, or markdown formatting. Your response must start with '[' and end with ']'.
    
    Example format: ["Unique Idea 1", "Unique Idea 2", "Unique Idea 3"]
    """
)

# Prompt 4: The main prompt to generate the full blog content
LAW_BLOG_GENERATION_PROMPT = ChatPromptTemplate.from_template(
    """
    You are an AI legal assistant specializing in Indian law. Your task is to write a comprehensive, well-structured, and clear blog post on the following topic.

    Blog Title: "{title}"

    Instructions:
    1.  **Structure:** The blog post must have an introduction, a main body with several sub-headings, and a concluding summary.
    2.  **Word Count:** Approximately 600-800 words.
    3.  **Tone:** Informative and professional, yet easy for a layperson to understand.
    4.  **Content:**
        * Explain the key legal concepts clearly.
        * If applicable, cite relevant sections of Acts (e.g., Section 438 of the CrPC) or Articles of the Constitution of India.
        * Do NOT invent case laws or section numbers. If you are not certain, state the general legal principle without specific citations.
    5.  **Formatting:** Use Markdown for formatting (headings, bold text, lists).
    6.  **Disclaimer:** MUST conclude the blog post with the following exact text: 'Disclaimer: This article is for informational purposes only and does not constitute legal advice. Please consult with a qualified legal professional for any specific issues.'

    Output only the complete blog text in Markdown format.
    """
)