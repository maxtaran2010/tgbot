import random

import telebot
from telebot import types
from secrets import apikey


bot = telebot.TeleBot(apikey, parse_mode=None)
words = {}
dword = ['Наверно да', 'нет', 'конечно']
mode = None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	global mode
	message: types.Message
	words.update({message.from_user.id: dword})
	bot.reply_to(message, "Добро пожаловать в бота-предсказаний! Нажмите на кнопку 'Задать вопрос' чтобы задать вопрос.")
	btn = types.KeyboardButton("Задать вопрос")
	btn2 = types.KeyboardButton("Добавить вариант ответа")
	btn3 = types.KeyboardButton("Все варианты ответа")
	btn4 = types.KeyboardButton("Удалить вариант ответа")
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(btn, btn2, btn3, btn4)
	bot.send_message(message.chat.id, reply_markup=markup, text='\\/')


@bot.message_handler(content_types=['text'])
def func(message):
	try:
		t = words[message.from_user.id]
	except:
		bot.reply_to(message, 'Вы не ввели команду /start')
		return

	global mode
	if message.text == "Задать вопрос":
		bot.reply_to(message, 'Напишите ваш вопрос: ')
		mode = "q"
	elif message.text == 'Добавить вариант ответа':
		bot.reply_to(message, 'Напишите ваш новый вариант ответа: ')
		mode = "a"
	elif message.text == "Все варианты ответа":
		bot.reply_to(message, ', '.join(words[message.from_user.id]))
	elif message.text == "Удалить вариант ответа":
		bot.send_message(message.chat.id, ', '.join(words[message.from_user.id]))
		bot.reply_to(message, 'напишите номер для удаления')
		mode = 'd'
	else:
		if mode == 'q':
			bot.reply_to(message, random.choice(words[message.from_user.id]))
			mode = None
		if mode == 'a':
			words[message.from_user.id].append(message.text)
			bot.reply_to(message, 'Готово!')
		if mode == 'd':
			try:
				words[message.from_user.id].pop(int(message.text)-1)
			except:
				bot.reply_to(message, "ошибка")
			bot.reply_to(message, "Готово")


bot.infinity_polling()
