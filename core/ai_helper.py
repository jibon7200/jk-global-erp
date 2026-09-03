import google.generativeai as genai
from django.conf import settings


def ask_ai(instruction, context_text=""):
    """
    Sends a request to Google Gemini (free tier) to generate or
    rewrite text based on the user's instruction.

    - instruction: what the user wants (e.g. "Make this more formal",
      "Write a paragraph about milk business growth", "Summarize this")
    - context_text: existing text to work with (optional — empty for
      pure generation from scratch)

    Returns the AI's text response, or raises an Exception with a
    clear message if the API key is missing or the request fails.
    This function NEVER modifies any document/PDF directly — it only
    returns suggested text; the user must review and insert it
    themselves (per the project's rule that AI must never edit
    business data automatically without confirmation).
    """
    if not settings.GEMINI_API_KEY:
        raise Exception(
            "Gemini API key is not configured. Please add GEMINI_API_KEY to your .env file."
        )

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

    if context_text:
        prompt = (
            f"You are helping edit a document that may contain Bangla and/or English text.\n"
            f"Existing text:\n\"\"\"\n{context_text}\n\"\"\"\n\n"
            f"Instruction: {instruction}\n\n"
            f"Reply with ONLY the resulting text — no explanation, no quotes, no extra commentary."
        )
    else:
        prompt = (
            f"You are helping write content for a document that may need Bangla and/or English text.\n"
            f"Instruction: {instruction}\n\n"
            f"Reply with ONLY the generated text — no explanation, no quotes, no extra commentary."
        )

    response = model.generate_content(prompt)
    return response.text.strip()