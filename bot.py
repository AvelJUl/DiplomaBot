import gettext

import telebot
from telebot.types import Message

import config
from utils import messages, additional_messages, db

bot = telebot.TeleBot(config.TOKEN)


def translate(func):
    def wrapper(call):
        chat_id = (
            call.chat.id if isinstance(call, Message) else call.message.chat.id
        )
        lang_code = _db.select_language(chat_id) or config.DEFAULT_LANGUAGE
        lang = gettext.translation('messages', localedir='locale',
                                   languages=[lang_code])
        lang.install()
        func(call, lang.gettext, lang_code)
    return wrapper


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_en = telebot.types.InlineKeyboardButton(text='English',
                                                callback_data='en')
    btn_ru = telebot.types.InlineKeyboardButton(text='Русский',
                                                callback_data='ru')
    btn_zh = telebot.types.InlineKeyboardButton(text='中國人',
                                                callback_data='zh')
    keyboard.add(btn_ru, btn_en, btn_zh)
    bot.send_message(message.chat.id,
                     messages.START_MESSAGE,
                     parse_mode='HTML',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
@translate
def send_help(message, locale, lang=None):
    _ = locale
    bot.send_message(message.chat.id,
                     _(messages.HELP_MESSAGE),
                     parse_mode='HTML')


@bot.message_handler(commands=['lang'])
@translate
def send_help(message, locale, lang):
    _ = locale
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_en = telebot.types.InlineKeyboardButton(text='English',
                                                callback_data='en')
    btn_ru = telebot.types.InlineKeyboardButton(text='Русский',
                                                callback_data='ru')
    btn_zh = telebot.types.InlineKeyboardButton(text='中國人',
                                                callback_data='zh')
    keyboard.add(btn_ru, btn_en, btn_zh)
    bot.send_message(message.chat.id,
                     messages.LANGUAGE_CHOICE_MESSAGE,
                     parse_mode='HTML',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ('en', 'ru', 'zh'))
def callback_worker_lang(call):
    def func(call, locale, lang):
        _ = locale
        bot.send_message(call.message.chat.id,
                         _(messages.HELP_MESSAGE),
                         parse_mode='HTML')
    lang = call.data
    _db.insert_language(call.message.chat.id, lang)

    translate(func)(call)


@bot.message_handler(commands=['questions'])
@translate
def send_help(message, locale, lang=None):
    _ = locale
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for index, question in enumerate(messages.QUESTIONS_AND_ANSWERS.keys()):
        if lang in messages.QUESTIONS_AND_ANSWERS[question]['lang']:
            keyboard.add(
                telebot.types.InlineKeyboardButton(
                    text=_(question),
                    callback_data=str(index))
            )
    bot.send_message(message.chat.id,
                     _(messages.QUESTIONS_MESSAGE),
                     parse_mode='HTML',
                     reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call:
    call.data in list(
        map(str, range(0, len(messages.QUESTIONS_AND_ANSWERS.keys())))
    ) + list(
        map('add_{}'.format, range(0, len(additional_messages.QUESTIONS_AND_ANSWERS.keys())))
    )
)
@translate
def callback_worker_answer(call, locale, lang=None):
    _ = locale
    data = str(call.data)
    if data.startswith('add_'):
        data = data.replace('add_', '')
        message = list(
            additional_messages.QUESTIONS_AND_ANSWERS.items()
        )[int(data)]
        bot.send_message(call.message.chat.id,
                         "<b>" + _(message[0]) + "</b>\n\n"
                         + _(message[1]),
                         parse_mode='HTML')
    else:
        message = list(messages.QUESTIONS_AND_ANSWERS.items())[int(data)]
        bot.send_message(call.message.chat.id,
                         "<b>" + _(message[0]) + "</b>\n\n"
                         + _(message[1]["message"]),
                         parse_mode='HTML')


@bot.message_handler(content_types=['text'])
@translate
def get_messages(message, locale, lang=None):
    if lang == 'ru':
        user_question = message.text

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

        matching_themes = additional_messages.find_matching_themes(
            user_question
        )

        if not matching_themes:
            bot.send_message(message.chat.id,
                             additional_messages.NO_ANSWER_MESSAGE,
                             parse_mode='HTML',
                             reply_markup=keyboard)
            return

        for index, question in enumerate(
                additional_messages.QUESTIONS_AND_ANSWERS.keys()
        ):
            if question in matching_themes:
                keyboard.add(
                    telebot.types.InlineKeyboardButton(
                        text=question,
                        callback_data='add_{}'.format(index))
                )

        bot.send_message(message.chat.id,
                         additional_messages.QUESTIONS_MESSAGE,
                         parse_mode='HTML',
                         reply_markup=keyboard)


_db = db.DataBase()
try:
    bot.polling()
except KeyboardInterrupt:
    _db.close()
