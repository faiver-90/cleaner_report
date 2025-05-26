from fastapi import FastAPI

from tg_router import router_main


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router_main)
    return app


app = get_app()
