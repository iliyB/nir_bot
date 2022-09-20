from aiogram.fsm.state import State, StatesGroup


class PhoneForm(StatesGroup):
    phone = State()
