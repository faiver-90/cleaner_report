import json
import logging

from fastapi import APIRouter, HTTPException

from api.v1.utils import send_request
import api.v1.configs.log_conf

logger = logging.getLogger(__name__)

v1 = APIRouter()


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}


@v1.post("/send_jwt/{token:str}")
async def send_jwt(token: str):
    data = {"code": token}
    try:
        response = await send_request(
            method="post",
            url="http://auth_service:8001/check_jwt",
            json=data
        )
        response_data = response.json()
        raise HTTPException('jhkдh')
        logger.info(f"Token sent: {token}, response: {response_data}")
        return {"code_response": response_data.get("jwt")}

    except json.JSONDecodeError as e:
        logger.error(f"Ответ от auth_service не является JSON: {e}")
        raise HTTPException(status_code=502, detail="Invalid response "
                                                    "format from auth_service")

    except HTTPException as e:
        logger.warning(f"Ошибка при запросе к auth_service: {e.detail}")
        raise

    except Exception as e:
        logger.exception(f"Неожиданная ошибка при обработке send_jwt: {e}")
        raise HTTPException(status_code=500, detail="Internal error")
