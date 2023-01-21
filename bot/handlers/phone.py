from typing import Match

import aiogram
import utils
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputFile, Message
from commands import CommandEnum
from keyboards.inlines import generate_inline_keyboard_for_links
from our_types import ObservedStrObject
from services.cards import CardService
from services.parser.main import parser_main
from services.search import SearchService
from states import ObjectForm

from bot import bot

phone_router = Router()


@phone_router.message(commands=[CommandEnum.PHONE.name.lower()])
async def phone_form(message: Message, state: FSMContext) -> None:
    await state.set_state(ObjectForm.phone)
    await message.answer("Введите номер, начиная с 7")


@phone_router.message(
    F.text.regexp(r"7([0-9]){10}").as_("phone_number"), state=ObjectForm.phone
)
async def set_phone(
    message: Message, state: FSMContext, phone_number: Match[str]
) -> None:

    obj = await SearchService().search_in_db(phone_number.string)

    utils.work_with_names(obj)
    utils.work_with_addresses(obj)
    utils.work_with_number(obj)

    parser_main(obj)

    obj.searched_by.add(phone_number.string)

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


@phone_router.message(state=ObjectForm.phone)
async def uncorrected_email(message: Message, state: FSMContext) -> None:
    await message.answer("Некорректный номер телефона")
