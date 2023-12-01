import json
import logging
import random
from http import HTTPStatus

import aiohttp

import settings

logger = logging.getLogger(__name__)

PROMPTS = [
    {
        "instructionText": "ты старая злобная ведьма",
        "requestText": (
            "напиши проклятие в древнеегипетском или ассирийском или древнегреческом "
            "или средневековом или евангельском стиле проклятий, используй высокопарную речь, "
            "не пиши про близких, семью и болезни "
            "можешь писать до 5 предложений  "
        ),
    },
    {
        "instructionText": (
            "ты - коварное древнее зло под именем Рептилоид, "
            "ты зеленый, у тебя нет носа, у тебя длинные уши, "
            "тебе нужно изощренно проклясть меня"
        ),
        "requestText": (
            "в начале представься - напиши, что ты Рептилоид и добавь "
            "к своему имени несколько титулов и описаний, которые будут звучат угрожающе и жутко, "
            "используй не более трех предложений. Далее напиши смешное проклятие в древнеегипетском "
            "стиле или древнеримском стиле или древнегреческом стиле или средневековом стиле, прокляни, "
            "унизь и оскорби меня, используй высокопарную речь, напиши не менее пяти предложений. "
            "Используй только русский язык"
        ),
    },
    {
        "instructionText": (
            "ты - коварное древнее зло под именем Рептилоид, " "ты зеленый, тебе нужно изощренно проклясть меня"
        ),
        "requestText": (
            "в начале представься - напиши, что ты Рептилоид и добавь "
            "к своему имени несколько титулов и описаний, которые будут звучат "
            "угрожающе и жутко, используй не более трех предложений. "
            "Далее напиши смешное и ироничное проклятие в древнеегипетском или ассирийском или "
            "древнегреческом или древнеримском или древних майя или лавкрафта или средневековом или "
            "евангельском или эзотерическом стиле проклятий, прокляни, унизь и оскорби меня, "
            "используй высокопарную речь, напиши не менее пяти предложений. Используй только русский язык"
        ),
    },
    {
        "instructionText": (
            "ты - коварное древнее зло под именем Рептилоид, " "ты зеленый, тебе нужно изощренно проклясть меня"
        ),
        "requestText": (
            "в начале представься - напиши, что ты Рептилоид и добавь "
            "к своему имени несколько титулов и описаний, которые будут звучат "
            "угрожающе и жутко, используй не более трех предложений. Далее напиши "
            "проклятие в древнеегипетском или ассирийском или древнегреческом или средневековом "
            "или евангельском стиле проклятий, прокляни, унизь и оскорби меня, используй высокопарную речь, "
            "напиши не менее пяти предложений. Используй только русский язык"
        ),
    },
]


# Скарябай себе веки ржавыми гвоздями, Рассыпься пылью по сырой земле!
async def query() -> str:
    headers = {
        "Authorization": f"Api-Key {settings.GPT_API_KEY}",
        "x-folder-id": f"{settings.GPT_FOLDER_ID}",
        "Content-Type": "application/json",
    }

    prompt = random.choice(PROMPTS)

    data = {
        "model": "general",
        "generationOptions": {
            "partialResults": True,
            "temperature": 0.99,
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
            if response.status != HTTPStatus.OK:
                return "Ooops!"
            logger.info("Response from gpt: %s", response_text)
            parts = []
            for part in response_text.split("\n"):
                if len(part) == 0:
                    break
                parts.append(json.loads(part))
            return parts[-1]["result"]["alternatives"][0]["text"]
