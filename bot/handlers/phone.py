# import phonenumbers
# from aiogram import Router
# from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.types import Message
# from aiogram.utils.markdown import hbold
#
# from commands import CommandEnum
# from handlers.person import person_router
# from parsing import wb_parse, avito_parse, vk_parse, delivery_parse, ya_parse
# from states import PhoneForm
#
# phone_router = Router()
#
# @phone_router.message(commands=[CommandEnum.PHONE.name.lower()])
# async def phone_form(message: Message, state: FSMContext) -> None:
#     await state.set_state(PhoneForm.phone)
#     await message.answer("Введите номер, начиная с 7")
#
#
# @person_router.message(PhoneForm.phone)
# async def end_phone_form(message: Message, state: FSMContext) -> None:
#     phone = phonenumbers.PhoneNumberMatcher(message.text, "IN")
#     if not phone:
#         await message.answer("Введен некорректный номер")
#     else:
#         await state.clear()
#         await message.answer(f"Введенный номер - {phone.text}")
#         await message.answer("Парсим wildberries...")
#         wb_result = await wb_parse(phone.text)
#         if not wb_result:
#             await message.answer("Записей не найдено")
#         else:
#             wb_card = (
#                 f"id: {hbold(wb_result.get('_wildberries_id'))}\n"
#                 f"ФИО: {hbold(wb_result.get('wildberries_name'))}\n"
#                 f"email: {hbold(wb_result.get('wildberries_email'))}\n"
#                 f"Адрес офиса: {hbold(wb_result.get('wildberries_address'))}\n"
#             )
#             await message.answer(wb_card)
#
#         await message.answer("Парсим avito...")
#         avito_result = await avito_parse(phone.text)
#         if not avito_result:
#             await message.answer("Записей не найдено")
#         else:
#             for order in avito_result:
#                 avito_card = (
#                     f"id заказа: {hbold(order.get('_avito_id'))}\n"
#                     f"Имя: {hbold(order.get('avito_user_name'))}\n"
#                     f"Локация: {hbold(order.get('avito_user_location'))}\n"
#                     f"Название: {hbold(order.get('avito_ad_title'))}\n"
#                     f"Опубликовано: {hbold(order.get('avito_ad_pdate'))}\n"
#                     f"Адрес офиса: {hbold(order.get('wildberries_address'))}\n"
#                 )
#                 await message.answer(avito_card)
#
#         await message.answer("Парсим delivery...")
#         delivery_result = await delivery_parse(phone.text)
#         if not delivery_result:
#             await message.answer("Записей не найдено")
#         else:
#             for order in delivery_result:
#                 avito_card = (
#                     f"id: {hbold(order.get('_delivery_id'))}\n"
#                     f"Имя: {hbold(order.get('delivery_name'))}\n"
#                     f"Локация: {hbold(order.get('delivery_address'))}\n"
#                     f"Дата: {hbold(order.get('delivery_created'))}\n"
#                     f"Стоимость заказа: {hbold(order.get('delivery_amount_rub'))}\n"
#                     f"Суммарная стоимость заказов: {hbold(order.get('delivery_total_rub'))}\n"
#                     f"Номер заказа: {hbold(order.get('_delivery_seq_pn_geo_count'))}\n"
#                 )
#                 await message.answer(avito_card)
#
#         await message.answer("Парсим Яндекс еда...")
#         ya_result = await ya_parse(phone.text)
#         if not ya_result:
#             await message.answer("Записей не найдено")
#         else:
#             for order in ya_result:
#                 locate = f"{order.get('yandex_address_city')} {order.get('yandex_address_street')} дом {order.get('yandex_address_house')} кв {order.get('yandex_address_office')}"
#                 avito_card = (
#                     f"id: {hbold(order.get('_yandex_id'))}\n"
#                     f"Имя: {hbold(order.get('yandex_name'))}\n"
#                     f"Локация: {hbold(locate)}\n"
#                     f"Дата: {hbold(order.get('yandex_created_at'))}\n"
#                     f"Стоимость заказа: {hbold(order.get('yandex_amount_rub'))}\n"
#                     f"Суммарная стоимость заказов: {hbold(order.get('yandex_sum_orders'))}\n"
#                     f"Устройство: {hbold(order.get('yandex_user_agent'))}\n"
#                 )
#                 await message.answer(avito_card)
#
#         await message.answer("Парсим vk...")
#         vk_result = await vk_parse(phone.text)
#         if not vk_result:
#             await message.answer("Записей не найдено")
#         else:
#             vk_card = (
#                 f"id: {hbold(vk_result.get('_vk_id'))}\n"
#                 f"Имя: {hbold(vk_result.get('vk_first_name'))}\n"
#                 f"Фамилия: {hbold(vk_result.get('vk_last_name'))}\n"
#                 f"email: {hbold(vk_result.get('vk_email'))}\n"
#                 f"Пароль: {hbold(vk_result.get('vk_password'))}\n"
#             )
#             await message.answer(vk_card)
#
