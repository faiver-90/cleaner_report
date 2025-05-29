import httpx

API_URL = "http://auth_service:8001"


async def register_user(username, email, password):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        return resp.status_code, resp.json()
