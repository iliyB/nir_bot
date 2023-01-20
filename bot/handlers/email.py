from typing import Match

import utils
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from commands import CommandEnum
from keyboards.inlines import generate_inline_keyboard_for_links
from our_types import ObservedStrObject
from services.cards import CardService
from services.parser.main import parser_main
from services.search import SearchService
from states import ObjectForm

from bot import bot

email_router = Router()


@email_router.message(commands=[CommandEnum.PHONE.name.lower()])
async def email_form(message: Message, state: FSMContext) -> None:
    await state.set_state(ObjectForm.email)
    await message.answer("Введите емейл")


@email_router.message(
    F.text.regexp(r"[\w\.-]+@[\w\.-]+(\.[\w]+)+").as_("email"), state=ObjectForm.email
)
async def set_phone(message: Message, state: FSMContext, email: Match[str]) -> None:

    obj = await SearchService().search_in_db(email.string)

    parser_main(obj)
    utils.work_with_names(obj)
    utils.work_with_addresses(obj)
    utils.work_with_number(obj)

    card = CardService().create_card(obj)

    for info_param in ObservedStrObject.__annotations__.keys():
        try:
            await message.answer(getattr(card, info_param))
        except TelegramBadRequest:
            await message.answer(getattr(card, info_param)[:4000])
            await message.answer(getattr(card, info_param)[4000:8000])

    await state.set_state(ObjectForm.next_stage)
    await state.set_data({"obj": obj.dict()})

    photo = FSInputFile("map.png")

    await bot.send_photo(chat_id=message.chat.id, photo=photo)

    await message.answer(
        text="Что делать дальше?", reply_markup=generate_inline_keyboard_for_links(obj)
    )


@email_router.message(state=ObjectForm.email)
async def uncorrected_email(message: Message, state: FSMContext) -> None:
    await message.answer("Некорректный емейл")
