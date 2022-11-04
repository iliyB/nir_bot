from typing import Match

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from commands import CommandEnum
from our_types import ObservedStrObject
from services.cards import CardService
from services.search import SearchService
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

    obj = await SearchService().search_by_phone(phone_number.string)
    card = CardService().create_card(obj)

    for info_param in ObservedStrObject.__annotations__.keys():
        try:
            await message.answer(getattr(card, info_param))
        except TelegramBadRequest:
            await message.answer(getattr(card, info_param)[:4000])
            await message.answer(getattr(card, info_param)[4000:8000])

    await state.clear()
