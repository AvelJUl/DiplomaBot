from gettext import gettext as _

START_MESSAGE = """
Please select your language 🌍
"""

LANGUAGE_CHOICE_MESSAGE = _("""Пожалуйста, выберите язык интерфейса.""")

START_CHOICE_MESSAGE = _(
    """Добавьте свой фильтр квартир и получите актуальные предложения прямо сейчас!"""
)

START_CHOICE_BUTTON = _(
    """Добавить фильтр ▶"""
)

CITY_CHOICE_MESSAGE = _("""В каком городе вы ищите жилье? 🏡""")

SELECT_ALL_BUTTON = _("""Выбрать все ✅""")

UNDO_SELECT_ALL_BUTTON = _("""Отменить выбор всех ❌""")

CONTINUE_BUTTON = _("""Далее ⏩""")

DISTRICT_CHOICE_MESSAGE = _("""Выберите один или несколько районов 🏙""")

ROOM_NUMBER_CHOICE_MESSAGE = _("""Выберите количество комнат 🔢""")

PRICE_CHOICE_MESSAGE = _("""Введите желаемую стоимость жилья <b>в злотых</b>
 (через дефис <b>в формате 2000-3000</b>) 💸""")

PRICE_ERROR_MESSAGE = _("""Сообщение об ошибке цены""")

CHOICE_DONE_MESSAGE = _("""Сообщение с информацией о выборе""")

UNSUBSCRIBE_MESSAGE = _("""Сообщение об успешной отмене уведомлений""")

LANGUAGE_CHOICE_DONE_MESSAGE = _("""Язык сменен.""")

HELP_MESSAGE = _("""
Доступные команды:
/lang - выбор языка инетерфейса
/help - справочное сообщение
/unsubscribe - отписка
/my_choice - просмотр параметров поиска
/change_my_choice - изменение параметров поиска
""")

KRAKOW_DISTRICTS = [
    {'text': '⚪  Mistrzejowice', 'callback_data': 'district_Mistrzejowice'},
    {'text': '⚪  Krowodrza', 'callback_data': 'district_Krowodrza'},
    {'text': '⚪  Nowa Huta', 'callback_data': 'district_Nowa-Huta'},
    {'text': '⚪  Zwierzyniec', 'callback_data': 'district_Zwierzyniec'},
    {'text': '⚪  Swoszowice', 'callback_data': 'district_Swoszowice'},
    {'text': '⚪  Podgórze', 'callback_data': 'district_Podgórze'},
    {'text': '⚪  Czyżyny', 'callback_data': 'district_Czyżyny'},
    {'text': '⚪  Bieńczyce', 'callback_data': 'district_Bieńczyce'},
    {'text': '⚪  Bronowice', 'callback_data': 'district_Bronowice'},
    {'text': '⚪  Prądnik Czerwony', 'callback_data': 'district_Prądnik-Czerwony'},
    {'text': '⚪  Prądnik Biały', 'callback_data': 'district_Prądnik-Biały'},
    {'text': '⚪  Podgórze Duchackie',
     'callback_data': 'district_Podgórze-Duchackie'},
    {'text': '⚪  Bieżanów-Prokocim',
     'callback_data': 'district_Bieżanów-Prokocim'},
    {'text': '⚪  Wzgórza Krzesławickie',
     'callback_data': 'district_Wzgórza-Krzesławickie'},
    {'text': '⚪  Łagiewniki-Borek Fałęcki',
     'callback_data': 'district_Łagiewniki-Borek-Fałęcki'}]

WARSAW_DISTRICTS = [
    {'text': '⚪  Bielany', 'callback_data': 'district_Bielany'},
    {'text': '⚪  Bemowo', 'callback_data': 'district_Bemowo'},
    {'text': '⚪  Białołęka',
     'callback_data': 'district_Białołęka'},
    {'text': '⚪  Wawer', 'callback_data': 'district_Wawer'},
    {'text': '⚪  Wesoła', 'callback_data': 'district_Wesoła'},
    {'text': '⚪  Wilanów', 'callback_data': 'district_Wilanów'},
    {'text': '⚪  Włochy', 'callback_data': 'district_Włochy'},
    {'text': '⚪  Wola', 'callback_data': 'district_Wola'},
    {'text': '⚪  Żoliborz', 'callback_data': 'district_Żoliborz'},
    {'text': '⚪  Mokotów', 'callback_data': 'district_Mokotów'},
    {'text': '⚪  Ochota', 'callback_data': 'district_Ochota'},
    {'text': '⚪  Praga Południe',
     'callback_data': 'district_Praga-Południe'},
    {'text': '⚪  Praga Północ',
     'callback_data': 'district_Praga-Północ'},
    {'text': '⚪  Rembertów',
     'callback_data': 'district_Rembertów'},
    {'text': '⚪  Śródmieście',
     'callback_data': 'district_Śródmieście'},
    {'text': '⚪  Targówek', 'callback_data': 'district_Targówek'},
    {'text': '⚪  Ursus', 'callback_data': 'district_Ursus'},
    {'text': '⚪  Ursynów', 'callback_data': 'district_Ursynów'}
]
