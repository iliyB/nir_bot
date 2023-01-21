import utils
from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from keyboards.inlines import LinkCallbackFactory, generate_inline_keyboard_for_links
from our_types import ObservedStrObject
from schemes.objects import ObservedObject
from services.cards import CardService
from services.parser.main import parser_main
from services.pdfs import generate_pdf_from_card
from services.search import SearchService
from states import ObjectForm

from bot import bot

common_router = Router()


@common_router.callback_query(LinkCallbackFactory.filter(), state=ObjectForm.next_stage)
async def next_stage(
    callback_query: CallbackQuery, callback_data: LinkCallbackFactory, state: FSMContext
) -> None:
    await bot.answer_callback_query(callback_query.id)

    obj = (await state.get_data()).get("obj")
    obj = ObservedObject.parse_obj(obj)

    obj = await SearchService().search_in_db(callback_data.link, obj)

    utils.work_with_names(obj)
    utils.work_with_addresses(obj)
    utils.work_with_number(obj)

    parser_main(obj)

    obj.searched_by.add(callback_data.link)

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


@common_router.callback_query(text="get_result", state=ObjectForm.next_stage)
async def get_result(callback_query: CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query.id)

    obj = (await state.get_data()).get("obj")

    card = CardService().create_card(ObservedObject.parse_obj(obj))
    pdf = types.input_file.BufferedInputFile(generate_pdf_from_card(card), "result.pdf")
    await callback_query.message.reply_document(pdf)

    await state.clear()
