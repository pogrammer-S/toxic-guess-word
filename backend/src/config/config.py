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
        DB_HOST=get_env_or_raise("DB_HOST", "PostgreSQL host"),
        DB_USER=get_env_or_raise("DB_USER", "PostgreSQL user"),
        DB_PASSWORD=get_env_or_raise("DB_PASSWORD", "PostgreSQL password"),
        DB_NAME=get_env_or_raise("DB_NAME", "PostgreSQL database name"),
        DB_PORT=int(os.getenv("DB_PORT", 5432)),
        MODEL_TOPN=int(os.getenv("MODEL_TOPN", 3))
    )