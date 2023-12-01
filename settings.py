import os

PORT = os.getenv("PORT", "443")

USE_SSL = os.getenv("USE_SSL", "YES")
CERT_FILE = os.getenv("CERT_FILE", "/etc/letsencrypt/live/reptiloid.fun/fullchain.pem")
KEY_FILE = os.getenv("KEY_FILE", "/etc/letsencrypt/live/reptiloid.fun/privkey.pem")

GPT_URL = os.getenv("GPT_URL", "https://llm.api.cloud.yandex.net/llm/v1alpha/instruct")
GPT_API_KEY = os.getenv("GPT_API_KEY")
GPT_FOLDER_ID = os.getenv("GPT_FOLDER_ID")

DATABASE_FILE = os.getenv("DATABASE_FILE", "database.db")
