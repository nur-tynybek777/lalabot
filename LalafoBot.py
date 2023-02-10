from aiogram import Dispatcher, Bot, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import bs4
from bs4 import BeautifulSoup
import time
import json
import asyncio
import os
import csv
import datetime
import sys


token = '6058684595:AAEmdjmLD1k1ifIA8zPlNIWFF8mltAvEsqI'
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

PATH = '.'

async def login(message: types.Message):
	group_chat_id = '-827050514'
	# group_chat_id = '-1001899323940'

	with open(f'{PATH}/appartments.json', 'r', encoding='utf-8') as file:
		appartments = json.load(file)

	appartments.pop('0')

	while True:
		for k,v in sorted(appartments.items()):
			table = f"ID: {hcode(k)} \nДата объявления: {hbold(v['created_time'])} \nКатегория: {hbold(v['category'])} \
			\nГород: {hbold(v['city'])} \nРайон: {hbold(v['district'])} \
			\nЦена: {hbold(v['price'])} {hbold(v['currency'])} \nВладелец: {hbold(v['user_name'])} \
			\nКонтакт: {hbold(v['mobile'])} \nОписание: {hbold(v['description'])} \
			\n\nВы также можете оставить свое объявление --> @nani_1622"
			image = hlink(' ', f'{v["image_url"]}\n')
			link = hlink(' ', f'{v["link"]}\n')
			await bot.send_message(group_chat_id, text = image + table + link)

			time.sleep(5)
		time.sleep(21600)


if __name__ == '__main__':
    asyncio.run(login('start'))
    executor.start_polling(dp)
