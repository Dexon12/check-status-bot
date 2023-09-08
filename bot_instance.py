import dotenv
import os
from aiogram import Bot

dotenv.load_dotenv('.env')

bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')