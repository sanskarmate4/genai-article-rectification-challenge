"""
Article Rectification System

This is where you implement your article rectification logic.
The run() function receives AI-generated content and should return the corrected version.

Feel free to:
- Add additional modules, classes, or helper functions
- Load and compare with source articles
- Implement multi-step validation and correction strategies
- Use multiple LLM calls or different models
- Add confidence scoring and logging
"""

from dotenv import load_dotenv
from litellm import completion
import os
import time

load_dotenv()

def run(source_content: str, ai_generated_content: str) -> str:
    """
    Rectify an AI-generated article.
    
    Args:
        source_content: The original source article text
        ai_generated_content: The AI-generated article text to be corrected
        
    Returns:
        str: The rectified article content
    """
    # # Create a simple prompt to fix issues
    prompt = f"""
    You are an expert factual editor.

    You are given:
    1. A SOURCE ARTICLE (ground truth).
    2. An AI GENERATED ARTICLE.

    Your goal is to make the AI-generated article factually identical to the source article while making the fewest possible edits.

    STRICT RULES:

    - Treat the AI-generated article as the base document.
    - Compare every factual claim against the source article.
    - Change ONLY text that is factually incorrect.
    - If a sentence is already factually correct, copy it exactly without changing even a single word.
    - Do NOT improve writing style.
    - Do NOT paraphrase.
    - Do NOT shorten or expand sentences.
    - Do NOT reorder paragraphs.
    - Do NOT change headings.
    - Do NOT change punctuation unless required to fix a factual error.
    - Preserve formatting exactly.
    - Only replace incorrect facts with the corresponding facts from the source article.

    Return ONLY the corrected article.
    Do not output markdown.
    Do not explain your reasoning.

    =========================
    SOURCE ARTICLE
    =========================

    {source_content}

    =========================
    AI GENERATED ARTICLE
    =========================

    {ai_generated_content}
    """    
    for attempt in range(3):
        try:
            response = completion(
                model=os.getenv("LLM_MODEL_NAME"),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                api_key=os.getenv("LLM_API_KEY"),
                api_base=os.getenv("LLM_API_BASE"),
                temperature=0,
                max_tokens=2500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < 2:
                time.sleep(2)
            else:
                raise

