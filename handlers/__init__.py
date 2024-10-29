from aiogram import Router, F

from .start import start_router
from .other_messages import other_msg_router
from .opros_dialog import opros_router
from .admin_book_fsm import admin_book_router
from .book_catalog import catalog_router
from .group_bot import group_router

private_router = Router()

private_router.include_router(start_router)
private_router.include_router(opros_router)
private_router.include_router(admin_book_router)
private_router.include_router(catalog_router)
# в самом конце общий обработчик
private_router.include_router(other_msg_router)

private_router.message.filter(F.chat.type == 'private')
private_router.callback_query.filter(F.chat.type == 'private')
