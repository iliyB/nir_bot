from aiogram.fsm.state import State, StatesGroup


class ObjectForm(StatesGroup):
    phone = State()
    next_stage = State()
