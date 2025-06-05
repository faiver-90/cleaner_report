from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from api import login_user

router = Router()


class LoginForm(StatesGroup):
    username = State()
    password = State()


@router.message(F.text.lower() == "/login")
async def start_login(msg: Message, state: FSMContext):
    await msg.answer("Введите имя пользователя:")
    await state.set_state(LoginForm.username)


@router.message(LoginForm.username)
async def login_username(msg: Message, state: FSMContext):
    await state.update_data(username=msg.text)
    await msg.answer("Введите пароль:")
    await state.set_state(LoginForm.password)


@router.message(LoginForm.password)
async def login_password(msg: Message, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    password = msg.text
    chat_id = str(msg.chat.id)

    status, result = await login_user(
        username=username,
        password=password,
        chat_id=chat_id
    )

    if status == 200:
        await state.update_data(token=result["access_token"])
        data = await state.get_data()
        token = data.get("token")
        await msg.answer(f"Добро пожаловать, {result['user']['username']}!")
        await msg.answer(f"Ваш токен в памяти, {token}!")
    else:
        await msg.answer(f"Ошибка входа: "
                         f"{result.get('message', 'неизвестно')}")

    await state.clear()
