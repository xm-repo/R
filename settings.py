import os

PORT = os.getenv("PORT", "443")

USE_SSL = os.getenv("USE_SSL", "YES")
CERT_FILE = os.getenv("CERT_FILE", "/etc/letsencrypt/live/reptiloid.fun/fullchain.pem")
KEY_FILE = os.getenv("KEY_FILE", "/etc/letsencrypt/live/reptiloid.fun/privkey.pem")
