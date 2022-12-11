from typing import Match

from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from commands import CommandEnum
from keyboards.inlines import LinkCallbackFactory, generate_inline_keyboard_for_links
from our_types import ObservedStrObject
from schemes.objects import ObservedObject
from services.cards import CardService
from services.pdfs import generate_pdf_from_card
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

    obj = await SearchService().search_by_phone(phone_number.string)
    # todo: должна быть обработка данных
    card = CardService().create_card(obj)

    for info_param in ObservedStrObject.__annotations__.keys():
        try:
            await message.answer(getattr(card, info_param))
        except TelegramBadRequest:
            await message.answer(getattr(card, info_param)[:4000])
            await message.answer(getattr(card, info_param)[4000:8000])

    await state.set_state(ObjectForm.next_stage)
    await state.set_data({"obj": obj.dict()})

    await message.answer(
        text="Что делать дальше?", reply_markup=generate_inline_keyboard_for_links(obj)
    )


@phone_router.callback_query(LinkCallbackFactory.filter(), state=ObjectForm.next_stage)
async def next_stage(
    callback_query: CallbackQuery, callback_data: LinkCallbackFactory, state: FSMContext
) -> None:
    await bot.answer_callback_query(callback_query.id)

    obj = (await state.get_data()).get("obj")
    obj = ObservedObject.parse_obj(obj)

    if callback_data.type_link == "phone":
        obj = await SearchService().search_by_phone(callback_data.link, obj)

    # todo: должна быть обработка данных
    card = CardService().create_card(obj)

    for info_param in ObservedStrObject.__annotations__.keys():
        try:
            await callback_query.message.answer(getattr(card, info_param))
        except TelegramBadRequest:
            try:
                await callback_query.message.answer(getattr(card, info_param)[:4000])
                await callback_query.message.answer(
                    getattr(card, info_param)[4000:8000]
                )
            except TelegramBadRequest:
                await callback_query.message.answer(getattr(card, info_param)[:4000])
                await callback_query.message.answer(
                    getattr(card, info_param)[4000:8000]
                )
                await callback_query.message.answer(
                    getattr(card, info_param)[8000:12000]
                )

    await state.set_data({"obj": obj.dict()})

    await callback_query.message.answer(
        text="Что делать дальше?", reply_markup=generate_inline_keyboard_for_links(obj)
    )


@phone_router.callback_query(text="get_result", state=ObjectForm.next_stage)
async def get_result(callback_query: CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query.id)

    obj = (await state.get_data()).get("obj")

    card = CardService().create_card(ObservedObject.parse_obj(obj))
    pdf = types.input_file.BufferedInputFile(generate_pdf_from_card(card), "result.pdf")
    await callback_query.message.reply_document(pdf)

    await state.clear()
