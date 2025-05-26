import logging
import os
from logging.handlers import RotatingFileHandler

os.makedirs("tg_logs", exist_ok=True)

# Создаём обработчик с ротацией
handler = RotatingFileHandler(
    filename='tg_logs/logs.log',
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5
)

# Настройка формата логов
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
handler.setFormatter(formatter)

# Базовая настройка логгера
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[handler]
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
