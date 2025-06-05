from aiogram import Router

from handlers import login, photo, register

main_router = Router()
main_router.include_router(login.router)
main_router.include_router(photo.router)
main_router.include_router(register.router)

