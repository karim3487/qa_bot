import subprocess

from environs import Env

VERSION = subprocess.check_output(["git", "describe", "--always"]).strip().decode()

env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")
DEV_ID: str = env.str("DEV_ID")
ADMIN_CHAT_ID: str = env.str("ADMIN_CHAT_ID")
SUPPORT_CHAT_ID: str = env.str("SUPPORT_CHAT_ID")

LOGGING_LEVEL: int = env.int("LOGGING_LEVEL", 10)

AUTORESPONDER_API_KEY: str = env.str("AUTORESPONDER_API_KEY", "Please, set API key")
AUTORESPONDER_BASE_URL: str = env.str(
    "AUTORESPONDER_BASE_URL", "Please, set base url for auto responder"
)
