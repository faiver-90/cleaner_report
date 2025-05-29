import httpx
from utils import send_request

BASE_URL = "http://auth_service:8001"


async def register_user(username: str, email: str, password: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )
        return resp.status_code, resp.json()


async def login_user(username: str, password: str, chat_id: str):
    try:
        response = await send_request(
            "POST",
            f"{BASE_URL}/login",
            json={
                "username": username,
                "password": password,
                "chat_id": chat_id
            }
        )
        return response.status_code, response.json()
    except Exception as e:
        return 401, {"message": str(e)}
