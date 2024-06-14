from aiogram import Bot, Dispatcher
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.memory import MemoryStorage
from init_db import DB

storage = MemoryStorage()
API_TOKEN = '7075127081:AAFLuEc4Yzu9SsQj0446hA-m85udcf5rlxQ' #Введите токен бота

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
db = DB("users.db")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)
logging.basicConfig(level=logging.INFO)
