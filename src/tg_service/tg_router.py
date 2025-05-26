# from starlette.responses import JSONResponse
from fastapi import APIRouter

router_main = APIRouter()


@router_main.get('/')
async def test_connection():
    return {'It\'s': 'Work'}
