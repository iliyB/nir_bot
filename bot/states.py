from aiogram.fsm.state import State, StatesGroup


class ObjectForm(StatesGroup):
    phone = State()
    email = State()
    next_stage = State()
