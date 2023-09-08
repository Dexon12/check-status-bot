from aiogram import Router
from aiogram import types
from aiogram.filters import Text

from Bot.DataBase.db import UserService
from Bot.DataBase.redis_db import UserRedisService
cb_router = Router()    
flags = {'throttling_key': 'default'}


@cb_router.callback_query(Text('I_am_work'), flags=flags)
async def cb_work_today(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    answer = 'Yes'
    print('Before user_answer_rdb')
    await UserRedisService.user_answer_rdb(user_id, answer)
    await callback.message.answer('Ваш ответ сохранен')
    await callback.answer()


@cb_router.callback_query(Text('I_am_dont_work'), flags=flags)
async def cb_dont_work_today(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    answer = 'No'
    print('Before user_answer_rdb')
    await UserRedisService.user_answer_rdb(user_id, answer)
    await callback.message.answer('Ваш ответ сохранен')
    await callback.answer()


@cb_router.callback_query(Text('cb_confirm_send_form'), flags=flags)
async def cb_confirm_send_form(callback: types.CallbackQuery) -> None:
    """Callback answer to confirm data sent"""

    await callback.message.answer('Отлично вы зарегистрированы, уведомление будет приходить в 11 часов! Спасибо!')
    await callback.answer('Ваши данные отправлены')


@cb_router.callback_query(Text('delete_profile'), flags=flags)
async def cb_delete_profile(callback: types.CallbackQuery) -> None:
    await UserService.delete_all(callback.from_user.id)
    await callback.answer('Ваш профиль был удален')


@cb_router.callback_query(Text('dont_delete_profile'), flags=flags)
async def cb_dont_delete_profile(callback: types.CallbackQuery) -> None:
    await callback.message.answer('Круто, что ты решил с нами остаться!')
    await callback.answer()


@cb_router.callback_query(Text('AlertFalse'), flags=flags)
async def cb_alertfalse(callback: types.CallbackQuery) -> None:
    await callback.answer('Чтобы подписаться на рассылку напишите команду /registration')
    await callback.message.answer('Чтобы подписаться на рассылку напишите команду /registration')
