from google import genai
from django.conf import settings
from django.utils import timezone
from PIL import Image
from io import BytesIO


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

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

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

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )
    return response.text.strip()


def check_and_increment_ai_image_quota(user):
    """
    Checks if this user still has AI image generations left today.
    If yes, increments their counter and returns True.
    If the daily limit is reached, returns False WITHOUT incrementing.
    """
    from .models import AIImageUsage

    today = timezone.localdate()
    usage, _ = AIImageUsage.objects.get_or_create(user=user, date=today)

    if usage.count >= settings.AI_IMAGE_DAILY_LIMIT:
        return False

    usage.count += 1
    usage.save()
    return True


def generate_ai_image(prompt, reference_image_bytes=None):
    """
    Generates (or edits, if a reference image is given) an image
    using Google's free-tier "Nano Banana" model. Returns raw PNG
    bytes. This is NOT unlimited — callers MUST check the daily
    quota via check_and_increment_ai_image_quota() before calling
    this, to avoid unexpectedly hitting Google's usage limits.
    """
    if not settings.GEMINI_API_KEY:
        raise Exception(
            "Gemini API key is not configured. Please add GEMINI_API_KEY to your .env file."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    contents = [prompt]
    if reference_image_bytes:
        contents.append(Image.open(BytesIO(reference_image_bytes)))

    response = client.models.generate_content(
        model='gemini-2.5-flash-image',
        contents=contents
    )

    for part in response.parts:
        if part.inline_data is not None:
            return part.inline_data.data

    raise Exception("AI did not return an image. Try rephrasing your request.")