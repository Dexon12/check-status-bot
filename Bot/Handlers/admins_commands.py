from aiogram import types
from aiogram import Router
from aiogram.filters import Command


from Bot.middlewares.admin_middleware import AdminOnlyMiddleware
from Bot.DataBase.db import UserService
from Bot.DataBase.redis_db import UserRedisService

admin_command_router = Router()
admin_command_router.message.outer_middleware(AdminOnlyMiddleware())
admin_command_router.callback_query.outer_middleware(AdminOnlyMiddleware())
flags = {'throttling_key': 'default'}

# async def get_workers_command(message: types.Message) -> None:
#     admin_answers = {}
#     ids = set(await UserService.select_users_id())
#     ids_redis = await UserRedisService.get_user_answer_rdb()
#     if ids_redis:
#         for id in ids:
#             admin_answers[id] = []
#
#         for value in ids_redis:
#             id = int(value[0])
#             name, surname, nickname = await UserService.return_args(id)
#             admin_answers[id].append(f'Имя сотрудника: {name}\nФамилия сотрудника: {surname}\nНикнейм сотрудника: @{nickname}\n'
#                                      f'Работает сотрудник или нет: {value[1]}\n')
#
#         for id, answers in admin_answers.items():
#             await message.answer(text='\n'.join(answers))
#     else:
#         await message.answer(text='Пока никто не ответил :)')


@admin_command_router.message(Command('get_workers_list'), flags=flags)
async def get_workers_command(message: types.Message) -> None:
    admin_answers = []
    ids = await UserService.select_users_id()
    ids_redis = await UserRedisService.get_user_answer_rdb()
    print(ids_redis)
    if ids_redis:
        for user_id, answer in ids_redis:
            user_id = int(user_id)  # Преобразуем user_id в целое число
            name, surname, nickname = await UserService.return_args(user_id)
            admin_answers.append({
                'user_id': user_id,
                'name': name,
                'surname': surname,
                'nickname': nickname,
                'is_working': answer
            })
        if admin_answers:
            for answer in admin_answers:
                user_id = answer['user_id']
                name = answer['name']
                surname = answer['surname']
                nickname = answer['nickname']
                is_working = answer['is_working']
                response = (
                    f'Ответ для пользователя с ID {user_id}:\n'
                    f'Имя сотрудника: {name}\n'
                    f'Фамилия сотрудника: {surname}\n'
                    f'Никнейм сотрудника: @{nickname}\n'
                    f'Работает сотрудник или нет: {is_working}\n'
                )
                await message.answer(text=response)
        else:
            await message.answer('Пока никто не ответил :)')
    else:
        await message.answer('Пока никто не ответил :)')





# async def get_workers_command(message: types.Message) -> None:
#     admin_answers = {}
#     ids = set(await UserService.select_users_id())
#     ids_redis = await UserRedisService.get_user_answer_rdb()
#     print(ids)
#     if ids_redis:
#         for idi in ids:
#             for value in ids_redis:
#                 name, surname, nickname = await UserService.return_args(idi)
#                 admin_answers.append(f'Имя сотрудника: {name}\nФамилия сотрудника: {surname}\nНикнейм сотрудника: @{nickname}\n'
#                                      f'Работает сотрудник или нет: {value[1]}\n')
#         await message.answer(text='\n'.join(admin_answers))
#     else:
#         await message.answer('Пока никто не ответил :)')

