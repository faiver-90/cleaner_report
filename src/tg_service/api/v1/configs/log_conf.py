import logging
import os
from logging.handlers import RotatingFileHandler

os.makedirs("tg_logs", exist_ok=True)

# Общий формат логов
formatter = logging.Formatter("%(asctime)s "
                              "[%(levelname)s] "
                              "%(name)s:"
                              " %(message)s")

# 🔸 Handler для business логики
business_handler = RotatingFileHandler("tg_logs/business.log",
                                       maxBytes=5_000_000,
                                       backupCount=3)
business_handler.setLevel(logging.INFO)
business_handler.setFormatter(formatter)

# 🔸 Handler для ошибок
errors_handler = RotatingFileHandler("tg_logs/errors.log",
                                     maxBytes=5_000_000,
                                     backupCount=3)
errors_handler.setLevel(logging.ERROR)
errors_handler.setFormatter(formatter)

# Root обработчик
root_handler = RotatingFileHandler("tg_logs/common.log",
                                   maxBytes=5_000_000,
                                   backupCount=3)
root_handler.setLevel(logging.DEBUG)
root_handler.setFormatter(formatter)

# Логгер бизнес-логики
business_logger = logging.getLogger("business")
business_logger.setLevel(logging.INFO)
business_logger.addHandler(business_handler)

# (Не давать логгерам пробрасывать логи выше)
business_logger.propagate = False
errors_handler.propagate = False

# Root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(root_handler)

# Отключаем спам от сторонних библиотек
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
