
import json
import time

from google import genai
from google.genai import types

from app.core.config import get_settings


def audit_content(content: str, guidelines: list[dict]) -> dict:
    """
    Audit submitted content against active brand guidelines using Gemini AI.
    Retries temporary provider errors automatically.
    """

    settings = get_settings()

    if not settings.gemini_api_key:
        raise RuntimeError("Gemini API key is not configured.")

    client = genai.Client(api_key=settings.gemini_api_key)

    prompt = f"""
You are BrandShield AI, an AI-powered brand compliance auditor.

Your task is to check submitted content against the approved brand guidelines.

APPROVED BRAND GUIDELINES:
{json.dumps(guidelines, indent=2)}

SUBMITTED CONTENT:
{content}

Return a valid JSON object using exactly this structure:

{{
    "overall_status": "pass or needs_review",
    "summary": "A short explanation of the audit result",
    "findings": [
        {{
            "guideline": "Relevant guideline title",
            "severity": "low, medium, or high",
            "problem": "Explain the violation",
            "suggestion": "Explain how to fix it",
            "quoted_text": "Exact problematic text"
        }}
    ]
}}

IMPORTANT RULES:
1. Only identify violations of the supplied guidelines.
2. Do not invent brand guidelines.
3. Do not report compliant content as a violation.
4. If no violations exist, return an empty findings array.
5. Use needs_review when violations are found.
6. Use pass when no violations are found.
7. Return JSON only. Do not include Markdown.
"""

    response = None

    # Retry temporary Gemini failures up to 3 times.
    for attempt in range(3):
        try:
            response = client.models.generate_content(
               model="gemini-3.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )

            break

        except Exception as exc:
            error_text = str(exc).upper()

            temporary_error = any(
                term in error_text
                for term in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "READERROR",
                    "WINERROR 10053",
                    "TIMEOUT",
                ]
            )

            if not temporary_error or attempt == 2:
                raise

            # Wait 2 seconds, then 4 seconds before retrying.
            wait_seconds = 2 ** (attempt + 1)

            print(
                f"Gemini temporarily unavailable. "
                f"Retry {attempt + 1}/2 in {wait_seconds} seconds."
            )

            time.sleep(wait_seconds)

    if response is None or not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    # Convert Gemini JSON response into a Python dictionary.
    try:
        result = json.loads(response.text)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Gemini returned invalid JSON."
        ) from exc

    # Validate the main response structure.
    if not isinstance(result, dict):
        raise RuntimeError("Invalid Gemini response format.")

    if result.get("overall_status") not in ["pass", "needs_review"]:
        raise RuntimeError("Invalid audit status returned by Gemini.")

    if not isinstance(result.get("summary"), str):
        raise RuntimeError("Invalid audit summary returned by Gemini.")

    if not isinstance(result.get("findings"), list):
        raise RuntimeError("Invalid audit findings returned by Gemini.")

    # Validate every finding.
    required_fields = [
        "guideline",
        "severity",
        "problem",
        "suggestion",
        "quoted_text",
    ]

    for finding in result["findings"]:
        if not isinstance(finding, dict):
            raise RuntimeError("Invalid audit finding.")

        for field in required_fields:
            if not isinstance(finding.get(field), str):
                raise RuntimeError(
                    f"Invalid or missing finding field: {field}"
                )

        if finding["severity"] not in ["low", "medium", "high"]:
            raise RuntimeError("Invalid finding severity.")

    return result
