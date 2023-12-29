import ast
import json
import os

import requests
from aiogram.fsm.storage.redis import Redis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from api.connect import APIServer

PRODUCTION = ast.literal_eval(os.getenv('PRODUCTION'))

api = APIServer()

s_storage = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
    db=int(os.getenv('REDIS_STORAGE')),
)
s_storage_user = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
    db=int(os.getenv('REDIS_STORAGE_USER')),
)
client = Bot(
    token=os.getenv('PROD_BOT_TOKEN') if PRODUCTION else os.getenv('DEV_BOT_TOKEN'),
    parse_mode="HTML",
)

BITRIX_URL = os.getenv('BITRIX_URL')

storage = RedisStorage(redis=s_storage)
dp = Dispatcher(storage=storage)

# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)

text_file = open('conf/text.json', 'r', encoding='utf-8')
text = json.load(text_file)

BOT_LOGIN = 'TuneBot_bot' if PRODUCTION else 'DevTuneBot_bot'