# from aiogram import Router
# from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.types import Message
#
# from commands import CommandEnum
#
# menu_router = Router()
#
#
# @menu_router.message(commands=[CommandEnum.START.name.lower()])
# async def command_start(message: Message):
#     await message.answer("Нах")
#
#
# @menu_router.message(commands=[CommandEnum.RESET.name.lower()])
# async def command_reset(message: Message, state: FSMContext):
#     await message.answer("Состояние сброшено")
#     await state.clear()
