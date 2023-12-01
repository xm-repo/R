import contextlib
import json
import logging
import random
import sqlite3
from http import HTTPStatus

import aiohttp

import prompts
import settings

logger = logging.getLogger(__name__)


def save_response(request: str, response: str):
    with contextlib.closing(sqlite3.connect(settings.DATABASE_FILE)) as connection:
        with connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS responses (id integer PRIMARY KEY, request text, response text)"
            )
            connection.execute(f"INSERT INTO responses VALUES (NULL, '{request}', '{response}')")


def _get_random_response():
    with contextlib.closing(sqlite3.connect(settings.DATABASE_FILE)) as connection:
        with connection:
            cursor = connection.cursor()
            res = cursor.execute("SELECT response FROM responses ORDER BY RANDOM() LIMIT 1;")
            return res.fetchone()[0]


def get_random_response():
    try:
        return _get_random_response()
    except Exception:
        logging.exception("Error in get_random_response")
        return "Ooops!"


# Скарябай себе веки ржавыми гвоздями, Рассыпься пылью по сырой земле!
async def query() -> str:
    headers = {
        "Authorization": f"Api-Key {settings.GPT_API_KEY}",
        "x-folder-id": f"{settings.GPT_FOLDER_ID}",
        "Content-Type": "application/json",
    }

    prompt = random.choice(prompts.PROMPTS)

    data = {
        "model": "general",
        "generationOptions": {
            "partialResults": True,
            "temperature": random.choice([0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]),
            "maxTokens": 7400,
        },
        "instructionText": prompt["instructionText"],
        "requestText": prompt["requestText"],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            settings.GPT_URL,
            headers=headers,
            json=data,
        ) as response:
            response_text = await response.text()
            logger.info("Response from gpt: %s", response_text)

            if response.status != HTTPStatus.OK:
                return get_random_response()

            parts = []
            for part in response_text.split("\n"):
                if len(part) == 0:
                    break
                parts.append(json.loads(part))

            result = parts[-1]["result"]["alternatives"][0]["text"]
            save_response(json.dumps(data), result)

            return result
