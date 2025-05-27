from fastapi import FastAPI

from api.v1.auth_router import v1


def get_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello2": "World55"}
    # app.include_router(v1)
    return app

print('lol')

app = get_app()
