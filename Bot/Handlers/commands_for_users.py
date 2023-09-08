from aiogram import types
from aiogram import Router
from aiogram.filters import Command, StateFilter

from Bot.keyboards.ikb import delete_profile

ADMIN_LIST = [6018428620, 973459911]
command_router = Router()
flags = {'throttling_key': 'default'}


@command_router.message(StateFilter(None), Command("help"), flags=flags)
async def help_command(message: types.Message) -> None:
    id = message.from_user.id
    if id in ADMIN_LIST:
        await message.answer(f'Привет! Чтобы подписаться на уведомления напишите /registration \n,'
                             ' чтобы удалить себя введите /delete\n Для того чтобы открыть статус сотрудников напишите:'
                             f'/get_workers_list')
    else:
        await message.answer(f'Привет! Чтобы подписаться на уведомления напишите /registration \n,'
                             f' чтобы удалить себя введите /delete')
    await message.delete()


@command_router.message(Command('delete'), flags=flags)
async def delete_command(message: types.Message) -> None:
    await message.answer('Вы точно хотите удалить?', reply_markup=delete_profile())




