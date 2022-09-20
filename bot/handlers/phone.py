from typing import Match

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from commands import CommandEnum
from configs import db_settings
from db import CreatePoolException, DBPoolManager
from states import PhoneForm

phone_router = Router()


@phone_router.message(commands=[CommandEnum.PHONE.name.lower()])
async def phone_form(message: Message, state: FSMContext) -> None:
    await state.set_state(PhoneForm.phone)
    await message.answer("Введите номер, начиная с 7")


@phone_router.message(
    F.text.regexp(r"7([0-9]){10}").as_("phone_number"), state=PhoneForm.phone
)
async def set_phone(
    message: Message, state: FSMContext, phone_number: Match[str]
) -> None:
    await message.answer(phone_number.string)

    if not db_settings.DB_SUSHI_NAME:
        await state.clear()
        return

    try:
        pool = await DBPoolManager().get_connect(db_settings.DB_SUSHI_NAME)
    except CreatePoolException:
        await state.clear()
        await message.answer("Error: no connect to db")
        return

    async with pool.acquire() as connect:
        async with connect.cursor() as cursor:
            await cursor.execute(
                f"SELECT * FROM sushi_full WHERE phone_number = '{phone_number.string}'"
            )
            result = cursor.fetchall()
            print(result)
    # pool.close()
    # await pool.wait_closed()
    await state.clear()
