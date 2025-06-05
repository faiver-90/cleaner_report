from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(F.text.lower() == "/me")
async def get_me(msg: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get("token")

    if not token:
        await msg.answer("Вы не авторизованы.")
        return

    print(token)
