from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from api.v1.configs import exceprions_conf
from api.v1.tg_router import v1


def get_app() -> FastAPI:
    import api.v1.configs.log_conf

    app = FastAPI()

    app.add_exception_handler(RequestValidationError,
                              exceprions_conf.validation_exception_handler)
    app.add_exception_handler(HTTPException,
                              exceprions_conf.http_exception_handler)
    app.add_exception_handler(Exception,
                              exceprions_conf.generic_exception_handler)
    app.include_router(v1)
    return app


app = get_app()
