from functools import wraps
from fastapi import HTTPException
import json
import logging

logger = logging.getLogger(__name__)


def handle_internal_errors(default_status_code=500):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except KeyError as e:
                logger.error(f"KeyError: {e}")
                raise HTTPException(status_code=500,
                                    detail=f"Missing key: {e}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
                raise HTTPException(status_code=502,
                                    detail="Invalid JSON from service")
            except TypeError as e:
                logger.error(f"TypeError: {e}")
                raise HTTPException(status_code=500, detail="Type mismatch")
            except Exception as e:
                logger.exception(f"Unhandled internal error: {e}")
                raise HTTPException(status_code=default_status_code,
                                    detail="Internal server error")

        return wrapper

    return decorator
