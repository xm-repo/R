import json
import logging
from http import HTTPStatus

import aiohttp

import settings

logger = logging.getLogger(__name__)


# Скарябай себе веки ржавыми гвоздями, Рассыпься пылью по сырой земле!
async def query() -> str:
    headers = {
        "Authorization": f"Api-Key {settings.GPT_API_KEY}",
        "x-folder-id": f"{settings.GPT_FOLDER_ID}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "general",
        "generationOptions": {
            "partialResults": True,
            "temperature": 0.99,
            "maxTokens": 100,
        },
        "instructionText": "ты злобная ведьма",
        "requestText": (
            "напиши проклятие в древнеегипетском или ассирийском или древнегреческом "
            "или средневековом или евангельском стиле проклятий, используй высокопарную речь, "
            "не пиши про близких, семью и болезни "
            "можешь писать до 5 предложений  "
        ),
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            settings.GPT_URL,
            headers=headers,
            json=data,
        ) as response:
            response_text = await response.text()
            if response.status != HTTPStatus.OK:
                return "Ooops!"
            logger.info("Response from gpt: %s", response_text)
            parts = []
            for part in response_text.split("\n"):
                if len(part) == 0:
                    break
                parts.append(json.loads(part))
            return parts[-1]["result"]["alternatives"][0]["text"]
