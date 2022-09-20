from aiogram import Bot, Dispatcher
from configs import app_settings

bot = Bot(token=app_settings.API_TOKEN, parse_mode="HTML")
dp = Dispatcher()
