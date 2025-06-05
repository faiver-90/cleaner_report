from fastapi import FastAPI

from llm_router import v1


def get_app() -> FastAPI:
    app = FastAPI(title='LLM service',
                  summary='Сервис для обработки фото с убранной площади и '
                          'формирования отчета.',
                  version='v1')
    app.include_router(v1)
    return app


app = get_app()
