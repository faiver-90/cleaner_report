from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from api import send_photo_to_service

router = Router()


class PhotoForm(StatesGroup):
    waiting_for_photo = State()


@router.message(F.text.lower() == "/send_photo")
async def start_photo_upload(msg: Message, state: FSMContext):
    data = await state.get_data()

    if not data.get("access_token"):
        await msg.answer("Сначала выполните вход через /login.")
        await msg.answer(f"Текущее содержание data = {data}.")
        return

    await msg.answer("Пожалуйста, отправьте фото.")
    await state.set_state(PhotoForm.waiting_for_photo)


@router.message(PhotoForm.waiting_for_photo, F.photo)
async def receive_photo(msg: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get("access_token")

    photo = msg.photo[-1]
    file = await msg.bot.get_file(photo.file_id)
    file_url = \
        f"https://api.telegram.org/file/bot{msg.bot.token}/{file.file_path}"

    status_code, text = await send_photo_to_service(file_url, token)

    if status_code == 200:
        await msg.answer("Фото успешно отправлено.")
    else:
        await msg.answer(f"Ошибка отправки: {text}")

    await state.set_state(None)
