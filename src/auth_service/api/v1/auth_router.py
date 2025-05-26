from fastapi import APIRouter

v1 = APIRouter()


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}
