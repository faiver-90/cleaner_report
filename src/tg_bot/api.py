import httpx
from utils import send_request

AUTH_URL = "http://auth_service:8001"
LLM_URL = "http://llm_service:8002"


async def register_user(username: str, email: str, password: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{AUTH_URL}/register",
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
            f"{AUTH_URL}/login",
            json={
                "username": username,
                "password": password,
                "chat_id": chat_id
            }
        )
        return response.status_code, response.json()
    except Exception as e:
        return 401, {"message": str(e)}


async def send_photo_to_service(file_url: str, token: str):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        try:
            # Получаем байты файла
            file_response = await client.get(file_url)
            file_response.raise_for_status()

            files = {
                "file": ("photo.jpg", file_response.content, "image/jpeg")
            }

            resp = await client.post(
                f"{LLM_URL}/upload_photo",
                files=files,
                headers=headers
            )

            return resp.status_code, resp.text
        except Exception as e:
            return 500, str(e)
