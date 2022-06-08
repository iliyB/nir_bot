import phonenumbers
from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from commands import CommandEnum
from handlers.person import person_router
from parsing import wb_parse, avito_parse
from states import PhoneForm

phone_router = Router()

@phone_router.message(commands=[CommandEnum.PHONE.name.lower()])
async def phone_form(message: Message, state: FSMContext) -> None:
    await state.set_state(PhoneForm.phone)
    await message.answer("Введите номер, начиная с 7")


@person_router.message(PhoneForm.phone)
async def end_phone_form(message: Message, state: FSMContext) -> None:
    phone = phonenumbers.PhoneNumberMatcher(message.text, "IN")
    if not phone:
        await message.answer("Введен некорректный номер")
    else:
        await state.clear()
        await message.answer(f"Введенный номер - {phone.text}")
        await message.answer("Парсим wildberries...")
        wb_result = await wb_parse(phone.text)
        if not wb_result:
            await message.answer("Записей не найдено")
        else:
            wb_card = (
                f"id: {hbold(wb_result.get('_wildberries_id'))}\n"
                f"ФИО: {hbold(wb_result.get('wildberries_name'))}\n"
                f"email: {hbold(wb_result.get('wildberries_email'))}\n"
                f"Адрес офиса: {hbold(wb_result.get('wildberries_address'))}\n"
            )
            await message.answer(wb_card)

        await message.answer("Парсим avito...")
        avito_result = await avito_parse(phone.text)
        if not avito_result:
            await message.answer("Записей не найдено")
        else:
            for order in avito_result:
                avito_card = (
                    f"id заказа: {hbold(order.get('_avito_id'))}\n"
                    f"Имя: {hbold(order.get('avito_user_name'))}\n"
                    f"Локация: {hbold(order.get('avito_user_location'))}\n"
                    f"Название: {hbold(order.get('avito_ad_title'))}\n"
                    f"Опубликовано: {hbold(order.get('avito_ad_pdate'))}\n"
                    f"Адрес офиса: {hbold(order.get('wildberries_address'))}\n"
                )
                await message.answer(avito_card)

