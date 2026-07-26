import logging
from functools import lru_cache

import groq
from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL_NAME, LLM_TEMPERATURE

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_client() -> Groq:
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return Groq(api_key=GROQ_API_KEY)


def generate_answer(messages: list[dict]) -> str:
    client = get_client()
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=messages,
            temperature=LLM_TEMPERATURE,
        )
    except groq.RateLimitError as e:
        logger.warning("Groq rate limit hit: %s", e)
        raise RuntimeError(
            "The LLM API rate limit was reached. Please wait a moment and try again."
        ) from e
    except groq.APIConnectionError as e:
        logger.error("Could not reach Groq API: %s", e)
        raise RuntimeError("Could not reach the Groq API. Check your internet connection.") from e
    except groq.APIStatusError as e:
        logger.error("Groq API returned an error: %s", e)
        raise RuntimeError(f"The LLM API returned an error: {e.message}") from e

    return response.choices[0].message.content
