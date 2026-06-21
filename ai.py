import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_debrief(notes):

    prompt = f"""
You are a field intelligence analyst.

Analyze the following field visit notes.

Return ONLY valid JSON.

Required format:

{{
    "key_findings": "string",
    "blockers": "string",
    "sentiment": "string",
    "followups": "string",
    "tags": [
        "tag1",
        "tag2",
        "tag3"
    ]
}}

Do not add explanations.
Do not add markdown.
Do not add ```json.
Return only the JSON object.

Field Notes:
{notes}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    result = response.choices[0].message.content.strip()

    # Remove markdown wrappers if Groq adds them
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:
        return json.loads(result)

    except Exception:

        # fallback so app never crashes
        return {
            "key_findings": "AI parsing failed",
            "blockers": "",
            "sentiment": "",
            "followups": "",
            "tags": []
        }