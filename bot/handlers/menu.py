from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from commands import CommandEnum

menu_router = Router()


@menu_router.message(commands=[CommandEnum.START.name.lower()])
async def command_start(message: Message) -> None:
    await message.answer(
        (
            "Привет!\n"
            "Данный Telegram бот предстваляет собой систему информационного поиска данных о пользователях\n"
            "из открытых источников Интернета.\n"
            "Бот от имеет следующие команды:\n"
            "/start – описание бота\n"
            "/reset – сбросить текущий поиск;\n"
            "/phone – начать поиск по вводу номер телефона;\n"
            "/email – начать поиск по вводу электронного почтового ящика.\n"
            "Поисковая сессия может состоять из нескольких итераций:\n"
            "В том случае, если новых данных для поиска нет,\n"
            "система генерирует pdf файл с проведенным анализом и предоставляет возможность пользователя скачать его.\n"
            "Если новые данные - можно продолжить поиск.\n"
        )
    )


@menu_router.message(commands=[CommandEnum.RESET.name.lower()])
async def command_reset(message: Message, state: FSMContext) -> None:
    await message.answer("Состояние сброшено")
    await state.clear()
