import os
from types import SimpleNamespace
from dotenv import load_dotenv
load_dotenv()


def get_env_or_raise(var_name, description=None):
    value = os.getenv(var_name)
    if not value:
        msg = f"Не задана переменная окружения {var_name}" + (f" ({description})" if description else "")
        raise RuntimeError(msg)
    return value


def load_config():
    return SimpleNamespace(
        BOT_TOKEN=get_env_or_raise("BOT_TOKEN", "Telegram Bot API Token"),
        API_URL=get_env_or_raise("API_URL", "URL api в docker-compose")
    )