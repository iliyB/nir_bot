from aiogram.dispatcher.fsm.state import State, StatesGroup


class PersonForm(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    city = State()
    phone = State()


class PhoneForm(StatesGroup):
    phone = State()
