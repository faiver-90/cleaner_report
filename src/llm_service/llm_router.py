import random

from fastapi import APIRouter, UploadFile, File, HTTPException

v1 = APIRouter()


@v1.get('/test')
async def test():
    return {'test': 'work'}


@v1.post("/upload_photo")
async def upload_photo(file: UploadFile = File(...)):
    # Проверка MIME-типа
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400,
                            detail="Файл должен быть изображением.")

    contents = await file.read()  # можно сохранить или обработать
    result = random.choice([True, False])

    # Например, сохранить на диск (если нужно):
    # with open(f"photos/{file.filename}", "wb") as f:
    #     f.write(contents)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        'result': result
    }
