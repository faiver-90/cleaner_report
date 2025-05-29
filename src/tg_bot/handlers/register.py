from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from api import register_user

router = Router()


class RegForm(StatesGroup):
    username = State()
    email = State()
    password = State()


@router.message(F.text.lower() == "/register")
async def start_register(msg: Message, state: FSMContext):
    await msg.answer("Введите имя пользователя:")
    await state.set_state(RegForm.username)


@router.message(RegForm.username)
async def reg_username(msg: Message, state: FSMContext):
    await state.update_data(username=msg.text)
    await msg.answer("Введите email:")
    await state.set_state(RegForm.email)


@router.message(RegForm.email)
async def reg_email(msg: Message, state: FSMContext):
    await state.update_data(email=msg.text)
    await msg.answer("Введите пароль:")
    await state.set_state(RegForm.password)


@router.message(RegForm.password)
async def reg_password(msg: Message, state: FSMContext):
    data = await state.get_data()
    status, result = await register_user(
        username=data["username"],
        email=data["email"],
        password=msg.text
    )
    if status == 200:
        await msg.answer("Вы успешно зарегистрированы!")
    else:
        await msg.answer(f"Ошибка: {result.get('message', 'неизвестно')}")
    await state.clear()
