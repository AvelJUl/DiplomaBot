import re

import telebot
from collections import defaultdict

import config
from utils import messages, helpers, api as _api


bot = telebot.TeleBot(config.TOKEN)
api = _api.Api('https://unreal-estate.pl/', 'http://127.0.0.1:8987')
message_history = defaultdict(list)
asked_for_price = defaultdict(list)


######################
#       /start       #
######################
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn_en = telebot.types.InlineKeyboardButton(
        text='English 🇬🇧',
        callback_data='start_en',
    )
    btn_ru = telebot.types.InlineKeyboardButton(
        text='Русский 🇷🇺',
        callback_data='start_ru',
    )
    keyboard.row(btn_ru, btn_en)
    btn_pl = telebot.types.InlineKeyboardButton(
        text='Polski 🇵🇱',
        callback_data='start_pl',
    )
    btn_ua = telebot.types.InlineKeyboardButton(
        text='Українська 🇺🇦',
        callback_data='start_ua',
    )
    keyboard.row(btn_pl, btn_ua)
    result = bot.send_message(
        message.chat.id,
        messages.START_MESSAGE,
        parse_mode='HTML',
        reply_markup=keyboard,
    )
    message_history[message.chat.id].append(result.message_id)


######################
#       /help        #
######################
@bot.message_handler(commands=['help'])
def send_help(call):
    def func(message, locale):
        _ = locale
        bot.send_message(message.chat.id,
                         _(messages.HELP_MESSAGE),
                         parse_mode='HTML')
    helpers.translate(func)(call, api)


######################
#       /lang        #
######################
@bot.message_handler(commands=['lang'])
def send_lang(call):
    def func(message, locale):
        _ = locale
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn_en = telebot.types.InlineKeyboardButton(
            text='English 🇬🇧',
            callback_data='lang_en',
        )
        btn_ru = telebot.types.InlineKeyboardButton(
            text='Русский 🇷🇺',
            callback_data='lang_ru',
        )
        keyboard.row(btn_ru, btn_en)
        btn_pl = telebot.types.InlineKeyboardButton(
            text='Polski 🇵🇱',
            callback_data='lang_pl',
        )
        btn_ua = telebot.types.InlineKeyboardButton(
            text='Українська 🇺🇦',
            callback_data='lang_ua',
        )
        keyboard.row(btn_pl, btn_ua)
        result = bot.send_message(
            message.chat.id,
            _(messages.LANGUAGE_CHOICE_MESSAGE),
            parse_mode='HTML',
            reply_markup=keyboard,
        )
        message_history[message.chat.id].append(result.message_id)

    helpers.translate(func)(call, api)


######################
#    /unsubscribe    #
######################
@bot.message_handler(commands=['unsubscribe'])
def send_unsubscribe(call):
    def func(message, locale):
        _ = locale
        api.change_user(message.chat.id, is_notified=False)
        bot.send_message(
            message.chat.id,
            messages.UNSUBSCRIBE_MESSAGE,
            parse_mode='HTML'
        )
    helpers.translate(func)(call, api)


######################
#     /my_choice     #
######################
@bot.message_handler(commands=['my_choice'])
def send_my_choice(call):
    def func(message, locale):
        _ = locale
        data = api.get_user(message.chat.id)
        bot.send_message(
            message.chat.id,
            messages.CHOICE_DONE_MESSAGE + str(data),
            parse_mode='HTML'
        )
    helpers.translate(func)(call, api)


######################
# /change_my_choice  #
######################
@bot.message_handler(commands=['change_my_choice'])
def send_change_my_choice(call):
    def func(message, locale):
        _ = locale
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn_start_choice = telebot.types.InlineKeyboardButton(
            text=messages.START_CHOICE_BUTTON,
            callback_data='start_choice',
        )
        keyboard.add(btn_start_choice)

        chat_id = message.chat.id
        if message_history[chat_id]:
            bot.delete_message(
                chat_id, message_history[chat_id][-1]
            )
            message_history[chat_id].pop(-1)

        result = bot.send_message(
            chat_id,
            _(messages.START_CHOICE_MESSAGE),
            parse_mode='HTML',
            reply_markup=keyboard,
        )
        message_history[chat_id] = [result.message_id]

    helpers.translate(func)(call, api)


######################
#      callbacks     #
######################

after_choosing_lang_callback = (
    lambda call: 'lang_' in call.data
)
before_start_my_choice_callback = (
    lambda call: 'start_' in call.data and call.data != 'start_choice'
)
after_start_my_choice_callback = (
    lambda call: call.data == 'start_choice'
)
after_choosing_city_callback = (
    lambda call: 'city_' in call.data
)
choosing_district_callback = (
    lambda call: 'district_continue' != call.data and 'district_' in call.data
)
after_choosing_district_callback = (
    lambda call: 'district_continue' == call.data
)
choosing_room_callback = (
    lambda call: 'room_continue' != call.data and 'room_' in call.data
)
after_choosing_room_callback = (
    lambda call: 'room_continue' == call.data
)


@bot.callback_query_handler(func=after_choosing_lang_callback)
def after_choosing_lang_callback_function(call):
    def func(_call, locale):
        chat_id = _call.message.chat.id
        api.change_user(chat_id, language=_call.data.replace('lang_', ''))

        _ = locale
        helpers.hide_message(message_history, bot, chat_id)

        bot.send_message(
            chat_id,
            _(messages.LANGUAGE_CHOICE_DONE_MESSAGE),
            parse_mode='HTML',
        )

    helpers.translate(func)(call, api)


@bot.callback_query_handler(func=before_start_my_choice_callback)
def before_start_my_choice_callback_function(call):
    def func(_call, locale):


        _ = locale
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn_start_choice = telebot.types.InlineKeyboardButton(
            text=_(messages.START_CHOICE_BUTTON),
            callback_data='start_choice',
        )
        keyboard.add(btn_start_choice)

        chat_id = _call.message.chat.id
        helpers.hide_message(message_history, bot, chat_id)

        result = bot.send_message(
            chat_id,
            _(messages.START_CHOICE_MESSAGE),
            parse_mode='HTML',
            reply_markup=keyboard,
        )
        message_history[chat_id] = [result.message_id]

    chat_id = call.message.chat.id
    if not api.get_user(chat_id):
        api.create_user(chat_id, call.data.replace('start_', ''))
    else:
        api.change_user(chat_id, language=call.data.replace('start_', ''))

    helpers.translate(func)(call, api)


@bot.callback_query_handler(func=after_start_my_choice_callback)
def after_start_my_choice_callback_function(call):
    def func(_call, locale):
        _ = locale
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn_city_warsaw = telebot.types.InlineKeyboardButton(
            text='Warszawa',
            callback_data='city_Warszawa',
        )
        btn_city_krakow = telebot.types.InlineKeyboardButton(
            text='Kraków',
            callback_data='city_Kraków',
        )
        keyboard.row(btn_city_warsaw, btn_city_krakow)
        btn_city_empty = telebot.types.InlineKeyboardButton(
            text=_(messages.SELECT_ALL_BUTTON),
            callback_data='city_all',
        )
        keyboard.row(btn_city_empty)
        chat_id = _call.message.chat.id
        helpers.hide_message(message_history, bot, chat_id)

        result = bot.send_message(chat_id,
                         _(messages.CITY_CHOICE_MESSAGE),
                         parse_mode='HTML',
                         reply_markup=keyboard)
        message_history[chat_id].append(result.message_id)

    helpers.translate(func)(call, api)


@bot.callback_query_handler(func=after_choosing_city_callback)
def after_choice_city_callback_function(call):
    def func(_call, locale):
        chat_id = _call.message.chat.id

        if call.data != 'city_all':

            user_info = api.get_user(chat_id)
            preferences = user_info.get('preferences') or {}
            preferences.update(
                {'city__icontains': _call.data.replace('city_', '').lower()},
            )
            api.change_user(chat_id, preferences=preferences)

        _ = locale

        keyboard = telebot.types.InlineKeyboardMarkup()
        
        district_list = []
        if call.data == 'city_Warszawa':
            district_list = messages.WARSAW_DISTRICTS
        elif call.data == 'city_Kraków':
            district_list = messages.KRAKOW_DISTRICTS
        else:
            keyboard = telebot.types.InlineKeyboardMarkup()
            btn_room_1 = telebot.types.InlineKeyboardButton(
                text='⚪ 1',
                callback_data='room_1',
            )
            btn_room_2 = telebot.types.InlineKeyboardButton(
                text='⚪ 2',
                callback_data='room_2',
            )
            btn_room_3 = telebot.types.InlineKeyboardButton(
                text='⚪ 3',
                callback_data='room_3',
            )
            keyboard.row(
                btn_room_1,
                btn_room_2,
                btn_room_3,
            )
            btn_room_4 = telebot.types.InlineKeyboardButton(
                text='⚪ 4',
                callback_data='room_4',
            )
            btn_room_5 = telebot.types.InlineKeyboardButton(
                text='⚪ 5+',
                callback_data='room_5',
            )
            keyboard.row(
                btn_room_4,
                btn_room_5,
            )
            btn_room_all = telebot.types.InlineKeyboardButton(
                text=_(messages.SELECT_ALL_BUTTON),
                callback_data='room_all',
            )
            keyboard.row(
                btn_room_all,
            )
            helpers.hide_message(message_history, bot, _call.message.chat.id)
            chat_id = _call.message.chat.id
            if message_history[chat_id]:
                bot.delete_message(
                    chat_id, message_history[chat_id][-1]
                )
                message_history[chat_id].pop(-1)

            result = bot.send_message(
                call.message.chat.id,
                _(messages.ROOM_NUMBER_CHOICE_MESSAGE),
                parse_mode='HTML',
                reply_markup=keyboard)

            message_history[chat_id].append(result.message_id)
            return

        row = []
        for index, district in enumerate(district_list, start=1):
            row.append(telebot.types.InlineKeyboardButton(**district))
            if index % 3 == 0:
                keyboard.row(*row)
                row = []

        keyboard.row(telebot.types.InlineKeyboardButton(
            text=_(messages.SELECT_ALL_BUTTON),
            callback_data='district_all',
        ))

        chat_id = _call.message.chat.id
        helpers.hide_message(message_history, bot, chat_id)

        result = bot.send_message(
            chat_id,
            _(messages.DISTRICT_CHOICE_MESSAGE),
            parse_mode='HTML',
            reply_markup=keyboard)

        message_history[chat_id].append(result.message_id)

    helpers.translate(func)(call, api)


@bot.callback_query_handler(func=choosing_district_callback)
def choosing_district_callback_function(call):
    def func(_call, locale):
        _ = locale
        reply_markup = call.message.json.get('reply_markup') or {}

        rows = reply_markup.get('inline_keyboard') or []
        keyboard = helpers.prepare_new_keyboard('district', call.data, rows, _)
        bot.edit_message_reply_markup(
            call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    helpers.translate(func)(call, api)


@bot.callback_query_handler(func=after_choosing_district_callback)
def after_choosing_district_callback_function(call):
    def func(_call, locale):

        chat_id = _call.message.chat.id
        if call.data != 'district_all':
            user_info = api.get_user(chat_id)
            preferences = user_info.get('preferences') or {}
            reply_markup = call.message.json.get('reply_markup') or {}
            rows = reply_markup.get('inline_keyboard') or []
            districts = []
            for row in rows:
                for button in row:
                    if helpers.CHOSEN in button['text']:
                        districts.append(
                            button['callback_data'].replace('district_', ''),
                        )
            preferences.update(
                {'district__in': ','.join(districts)},
            )
            api.change_user(chat_id, preferences=preferences)

        _ = locale

        keyboard = telebot.types.InlineKeyboardMarkup()
        btn_room_1 = telebot.types.InlineKeyboardButton(
            text='⚪ 1',
            callback_data='room_1',
        )
        btn_room_2 = telebot.types.InlineKeyboardButton(
            text='⚪ 2',
            callback_data='room_2',
        )
        btn_room_3 = telebot.types.InlineKeyboardButton(
            text='⚪ 3',
            callback_data='room_3',
        )
        keyboard.row(
            btn_room_1,
            btn_room_2,
            btn_room_3,
        )
        btn_room_4 = telebot.types.InlineKeyboardButton(
            text='⚪ 4',
            callback_data='room_4',
        )
        btn_room_5 = telebot.types.InlineKeyboardButton(
            text='⚪ 5+',
            callback_data='room_5',
        )
        keyboard.row(
            btn_room_4,
            btn_room_5,
        )
        btn_room_all = telebot.types.InlineKeyboardButton(
            text=_(messages.SELECT_ALL_BUTTON),
            callback_data='room_all',
        )
        keyboard.row(
            btn_room_all,
        )

        helpers.hide_message(message_history, bot, _call.message.chat.id)
        if message_history[chat_id]:
            bot.delete_message(
                chat_id, message_history[chat_id][-1]
            )
            message_history[chat_id].pop(-1)

        result = bot.send_message(
            call.message.chat.id,
            _(messages.ROOM_NUMBER_CHOICE_MESSAGE),
            parse_mode='HTML',
            reply_markup=keyboard)

        message_history[chat_id].append(result.message_id)

    helpers.translate(func)(call, api)


@bot.callback_query_handler(func=choosing_room_callback)
def choosing_room_callback_function(call):
    def func(_call, locale):
        _ = locale
        reply_markup = call.message.json.get('reply_markup') or {}

        rows = reply_markup.get('inline_keyboard') or []
        keyboard = helpers.prepare_new_keyboard('room', call.data, rows, _)
        bot.edit_message_reply_markup(
            call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )

    helpers.translate(func)(call, api)


@bot.callback_query_handler(func=after_choosing_room_callback)
def after_choosing_room_callback_function(call):
    def func(_call, locale):
        chat_id = _call.message.chat.id
        if call.data != 'room_all':
            user_info = api.get_user(chat_id)
            preferences = user_info.get('preferences') or {}
            reply_markup = call.message.json.get('reply_markup') or {}
            rows = reply_markup.get('inline_keyboard') or []
            number_of_rooms = []
            for row in rows:
                for button in row:
                    if helpers.CHOSEN in button['text']:
                        number_of_rooms.append(
                            button['callback_data'].replace('room_', ''),
                        )
            preferences.update(
                {'number_of_rooms__in': ','.join(number_of_rooms)},
            )
            api.change_user(chat_id, preferences=preferences)

        _ = locale
        helpers.hide_message(message_history, bot, chat_id)
        result = bot.send_message(
            chat_id,
            _(messages.PRICE_CHOICE_MESSAGE),
            parse_mode='HTML',
        )
        asked_for_price[chat_id] = result.message_id
        message_history[chat_id].append(result.message_id)

    helpers.translate(func)(call, api)


@bot.message_handler(content_types=['text'])
def after_choosing_price_callback_function(call):
    def func(message, locale):
        _ = locale
        chat_id = message.chat.id
        if chat_id not in asked_for_price:
            bot.delete_message(
                chat_id, message.message_id
            )
            return

        pattern = r'[1-9]+\d{3}-[1-9]+\d{3,4}'
        match = re.fullmatch(pattern, message.text)

        if match is not None:
            price_lower, price_upper = list(map(int, message.text.split('-')))
            if price_upper < price_lower:
                if message_history[chat_id]:
                    bot.delete_message(
                        chat_id, message_history[chat_id][-1]
                    )
                    message_history[chat_id].pop(-1)
                result = bot.send_message(
                    chat_id,
                    _(messages.PRICE_ERROR_MESSAGE),
                    parse_mode='HTML',
                )
                asked_for_price[chat_id] = result.message_id
                message_history[chat_id].append(message.message_id)
                message_history[chat_id].append(result.message_id)

                return

            for message_id in message_history[chat_id]:
                bot.delete_message(
                    chat_id, message_id
                )

            bot.delete_message(
                chat_id, message.message_id
            )

            bot.send_message(
                chat_id,
                _(messages.CHOICE_DONE_MESSAGE),
                parse_mode='HTML',
            )
            asked_for_price.pop(chat_id)
            message_history.pop(chat_id)


            user_info = api.get_user(chat_id)
            preferences = user_info.get('preferences') or {}
            preferences.update(
                {
                    'price__gte': price_lower,
                    'price__lte': price_upper,
                },
            )
            api.change_user(chat_id, preferences=preferences)

            bot.send_message(
                chat_id,
                api.make_link_to_see_other(chat_id),
                parse_mode='HTML',
            )

            return

        if message_history[chat_id]:
            bot.delete_message(
                chat_id, message_history[chat_id][-1]
            )
            message_history[chat_id].pop(-1)
        result = bot.send_message(
            chat_id,
            _(messages.PRICE_ERROR_MESSAGE),
            parse_mode='HTML',
        )
        asked_for_price[chat_id] = result.message_id
        message_history[chat_id].append(result.message_id)

    helpers.translate(func)(call, api)


bot.polling()
