from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def subscribe():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подписаться на оповещения', callback_data='AlertTrue'), InlineKeyboardButton(
            text='Не подписываться', callback_data='AlertFalse')]
    ])
    return ikb


def everything_is_right():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='cb_confirm_send_form'), InlineKeyboardButton(text='Нет', callback_data='cb_cancel_send_form')]
    ])
    return ikb


def delete_profile():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='delete_profile'), InlineKeyboardButton(text='Нет', callback_data='dont_delete_profile')]
    ])
    return ikb


def do_you_work_today():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='I_am_work'), InlineKeyboardButton(text='Нет', callback_data='I_am_dont_work')]
    ])
    return ikb
