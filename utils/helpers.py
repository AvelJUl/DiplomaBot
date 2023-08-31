import gettext
import telebot

import config

NOT_CHOSEN = '⚪'
CHOSEN = '🟢'


def prepare_new_keyboard(step, chosen_callback_data, rows, locale):
    from . import messages

    keyboard = telebot.types.InlineKeyboardMarkup()
    any_selected = False
    if '_all' in chosen_callback_data:
        any_selected = True
        for row in rows:
            changed_row = []
            for button in row:
                if '_continue' in button['callback_data']:
                    continue

                if '_all' in button['callback_data']:
                    keyboard.row(telebot.types.InlineKeyboardButton(
                        locale(messages.UNDO_SELECT_ALL_BUTTON),
                        callback_data=f'{step}_clear',
                    ))
                    continue

                new_button = button.copy()
                new_button['text'] = new_button['text'].replace(
                    NOT_CHOSEN, CHOSEN,
                )

                changed_row.append(
                    telebot.types.InlineKeyboardButton(
                        **new_button,
                    )
                )

            if changed_row:
                keyboard.row(*changed_row)

    elif '_clear' in chosen_callback_data:
        for row in rows:
            changed_row = []
            for button in row:
                if '_continue' in button['callback_data']:
                    continue

                if '_clear' in button['callback_data']:
                    keyboard.row(telebot.types.InlineKeyboardButton(
                        messages.SELECT_ALL_BUTTON,
                        callback_data=f'{step}_all',
                    ))
                    continue

                new_button = button.copy()
                new_button['text'] = new_button['text'].replace(
                    CHOSEN, NOT_CHOSEN,
                )

                changed_row.append(
                    telebot.types.InlineKeyboardButton(
                        **new_button,
                    )
                )

            if changed_row:
                keyboard.row(*changed_row)

    else:
        all_selected = True
        for row in rows:
            changed_row = []
            for button in row:
                if '_continue' in button['callback_data']:
                    continue

                if '_clear' in button['callback_data'] and not all_selected:
                    keyboard.row(telebot.types.InlineKeyboardButton(
                        locale(messages.SELECT_ALL_BUTTON),
                        callback_data=f'{step}_all',
                    ))
                    continue

                if '_all' in button['callback_data'] and all_selected:
                    keyboard.row(telebot.types.InlineKeyboardButton(
                        locale(messages.UNDO_SELECT_ALL_BUTTON),
                        callback_data=f'{step}_clear',
                    ))
                    continue

                new_button = button.copy()

                if chosen_callback_data == button['callback_data']:
                    replaced = (
                        NOT_CHOSEN
                        if NOT_CHOSEN in new_button['text']
                        else CHOSEN
                    )
                    replacer = (
                        CHOSEN
                        if NOT_CHOSEN in new_button['text']
                        else NOT_CHOSEN
                    )
                    new_button['text'] = new_button['text'].replace(
                        replaced, replacer)

                if NOT_CHOSEN in new_button['text']:
                    all_selected = False
                elif CHOSEN in new_button['text']:
                    any_selected = True

                changed_row.append(
                    telebot.types.InlineKeyboardButton(
                        **new_button,
                    )
                )

            if changed_row:
                keyboard.row(*changed_row)

    if any_selected:
        keyboard.row(telebot.types.InlineKeyboardButton(
            text=locale(messages.CONTINUE_BUTTON),
            callback_data=f'{step}_continue',
        ))

    return keyboard


def hide_message(message_history, bot, chat_id):
    if message_history[chat_id]:
        bot.delete_message(
            chat_id, message_history[chat_id][-1]
        )
        message_history[chat_id].pop(-1)


def translate(func):
    def wrapper(call, api):
        chat_id = (
            call.chat.id
            if isinstance(call, telebot.types.Message)
            else call.message.chat.id
        )
        lang_code = (
            api.get_user(chat_id).get('language')
            or config.DEFAULT_LANGUAGE
        )
        lang = gettext.translation(
            'messages',
            localedir='locale',
            languages=[lang_code],
        )
        lang.install()
        func(call, lang.gettext)
    return wrapper
