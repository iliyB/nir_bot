from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schemes.objects import ObservedObject


class LinkCallbackFactory(CallbackData, prefix="callback_link"):  # type: ignore
    type_link: Literal["email", "phone"]
    link: str


def generate_inline_keyboard_for_links(obj: ObservedObject) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for phone in set(obj.phones):
        keyboard.button(
            text=phone,
            callback_data=LinkCallbackFactory(
                type_link="phone",
                link=phone,
            ),
        )

    for email in set(obj.emails):
        keyboard.button(
            text=email,
            callback_data=LinkCallbackFactory(
                type_link="email",
                link=email,
            ),
        )

    keyboard.adjust(3)
    keyboard.button(text="Получить результат", callback_data="get_result")

    return keyboard.as_markup()
