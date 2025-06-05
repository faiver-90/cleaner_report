from fastapi import FastAPI

from llm_router import v1


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(v1)
    return app


app = get_app()
