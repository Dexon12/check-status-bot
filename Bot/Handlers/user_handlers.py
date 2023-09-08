from aiogram.filters import Command, Text
from aiogram import Router, F
from aiogram import types
from datetime import datetime
from aiogram.fsm.context import FSMContext

from bot_instance import bot
from Bot.keyboards.ikb import subscribe, everything_is_right
from Bot.FSM.FSMcontent import AlertStates
from Bot.DataBase.db import UserService

user_router = Router()
flags = {'throttling_key': 'default'}


@user_router.message(Command('start'), flags=flags)
async def start_command(message: types.Message) -> None:
    """Start command handler """

    await message.answer('Привет! Я TexDocktor Bot, нам важно знать выходишь ли ты сегодня на работу, '
                         'мы можем получить эту информацию? :), чтобы зарегистрироваться нажмите /registration, '
                         'для получения доступа к остальным командам напишите /help')
    await message.delete()


@user_router.message(Command('registration'), flags=flags)
async def reg_cmd(message: types.Message, state: FSMContext) -> None:
    """Registration command handler"""
    all_users_id = await UserService.select_users_id()
    user_id = message.from_user.id
    await message.delete()
    if user_id in all_users_id:
        await message.answer('Вы уже зарегистрированы! Для получения списка команд напишите /help')
    else:
        await message.answer("Чтобы зарегистрироваться нажмите на кнопку", reply_markup=subscribe())
        print('Before set state')
        await state.set_state(AlertStates.name)


@user_router.message(AlertStates.name, F.text.regexp(r'[A-Z][a-z]+'))
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(
        name=message.text,
        user_id=message.from_user.id
    )

    await message.answer('Подскажите пожалуйста какая у вас фамилия?')
    await state.set_state(AlertStates.surname)


@user_router.message(AlertStates.surname)
async def set_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(AlertStates.nickname)
    await message.answer('Напишите пожалуйста ваш Никнейм')


@user_router.message(AlertStates.nickname)
async def set_finish(message: types.Message, state: FSMContext) -> None:
    await state.update_data(nickname=message.from_user.username)
    await message.answer('Спасибо, все готово')

    data = await state.get_data()

    await bot.send_message(message.from_user.id,
                           text=f"Все верно: Имя: {data['name']}, Фамилия: {data['surname']}?",
                           reply_markup=everything_is_right())

    await UserService.insert_user(data['user_id'], data['name'], data['surname'], data['nickname'],
                                  True, datetime.now())

    await state.clear()
    print(state)


@user_router.callback_query(Text('cb_cancel_send_form'))
async def cb_cancel_send_form(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Cancel the current state for sending form. Cancel confirmation"""

    if state:
        await state.clear()

    await callback.message.answer('Хорошо, попробуем еще раз')
    await state.set_state(AlertStates.name)
    await callback.message.answer('Подскажите пожалуйста как вас зовут?')


@user_router.callback_query(Text('AlertTrue'))
async def cb_alerttrue(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer('Вы подписались на рассылку!')
    await state.set_state(AlertStates.name)
    await callback.message.answer('Подскажите пожалуйста как вас зовут?')
