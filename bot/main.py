import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.types import BotCommand

from bot import dp, bot
from commands import CommandEnum
from handlers.menu import menu_router
from handlers.person import person_router


async def set_command(bot: Bot) -> None:
    commands = [
        BotCommand(command=CommandEnum.START.name.lower(), description=CommandEnum.START.value),
        BotCommand(command=CommandEnum.RESET.name.lower(), description=CommandEnum.RESET.value),
        BotCommand(command=CommandEnum.PERSON.name.lower(), description=CommandEnum.PERSON.value)
    ]
    await bot.set_my_commands(commands)


async def main():
    dp.include_router(menu_router)
    dp.include_router(person_router)
    await set_command(bot)
    await  dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
