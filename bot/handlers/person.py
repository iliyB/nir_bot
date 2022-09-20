# from aiogram import Router
# from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.types import Message
#
# from commands import CommandEnum
# from states import PersonForm
#
# person_router = Router()
#
# @person_router.message(commands=[CommandEnum.PERSON.name.lower()])
# async def first_name_person(message: Message, state: FSMContext) -> None:
#     await state.set_state(PersonForm.first_name)
#     await message.answer("Введите имя")
#
#
# @person_router.message(PersonForm.first_name)
# async def last_name_person(message: Message, state: FSMContext) -> None:
#     await state.update_data(first_name=message.text)
#     await state.set_state(PersonForm.last_name)
#     await message.answer("Введите фамилия")
#
#
# @person_router.message(PersonForm.last_name)
# async def age_person(message: Message, state: FSMContext) -> None:
#     await state.update_data(last_name=message.text)
#     await state.set_state(PersonForm.age)
#     await message.answer("Введите возраст")
#
#
# @person_router.message(PersonForm.age)
# async def city_person(message: Message, state: FSMContext) -> None:
#     await state.update_data(age=message.text)
#     await state.set_state(PersonForm.city)
#     await message.answer("Введите город")
#
#
# @person_router.message(PersonForm.city)
# async def phone_person(message: Message, state: FSMContext) -> None:
#     await state.update_data(city=message.text)
#     await state.set_state(PersonForm.phone)
#     await message.answer("Введите телефон")
#
#
# @person_router.message(PersonForm.phone)
# async def end_person(message: Message, state: FSMContext) -> None:
#     await state.update_data(phone=message.text)
#     await message.answer(f"Введенные данные - {await state.get_data()}")
#     await state.clear()
