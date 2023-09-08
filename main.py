import asyncio
import hupper

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import redis.asyncio as redis
from aiogram.fsm.storage.redis import RedisStorage

from bot_instance import bot
from Bot.utils.logger import setup_logger
from Bot.utils.config import load_config
from Bot.Handlers.user_handlers import user_router
from Bot.Handlers.callbacks_handlers import cb_router
from Bot.Handlers.commands_for_users import command_router
from Bot.Handlers.admins_commands import admin_command_router
from Bot.utils.sending_msg import send_msg
from Bot.DataBase.db import DataBaseEngine
from Bot.DataBase.redis_db import RedisHandler

logger = setup_logger('main_logger', 'main_logs.log')


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(user_router)
    dp.include_router(cb_router)
    dp.include_router(command_router)
    dp.include_router(admin_command_router)
    logger.info('[INFO]: HANDLERS HAVE BEEN CONNECTED')

async def starting():
    await send_msg()
    print('1234')



async def start_redis():
    """
    Starts redis client for the redis server instance. Manage connection pool and execute operations.
    """
    try:
        redis_handler = RedisHandler()
        await redis_handler.connect()
        print('redis_host has been connect')
    except Exception as _ex:
        logger.error(f'[ERROR]: AN EXCEPTION DURING REDIS STARTUP HAS OCCURRED. PLEASE REVISE THE CODE - {_ex}')
    else:
        logger.info(f'[INFO]: REDIS SECOND DATABASE HAS BEEN INITIALIZED SUCCESSFULLY')


async def main(bot: Bot) -> None:
    """The main Entry point to the program. Starts and initialize the main Router and other tasks.

    Args:
        bot (Bot): Bot instance of our program. 
    """
    print('fdsjkfj')
    config = load_config('.env')

    if config.tg_bot.redis:
        redis_cl = redis.Redis()
        storage = RedisStorage(redis_cl)
        print()

        logger.info('[INFO]: RedisStorage HAS SUCCESSFULLY BEEN LOADED AND CONNECTED TO THE SERVER! (localhost:6379)')
    else:
        storage = MemoryStorage()
        logger.info('[INFO]: MEMORY STORAGE HAS SUCCESSFULLY BEEN LOADED')

    dp = Dispatcher(
        storage=storage
    )
    register_routers(dp)
    engine = DataBaseEngine()
    await engine.create_db()
    # await engine.drop_table()
    try:
        task_dp = dp.start_polling(bot)
        task_pool = engine.get_pool()
        msg_task = asyncio.create_task(starting())
        await start_redis()
        await asyncio.gather(task_dp, task_pool, msg_task)  # Перенести pool и адаптировать код
    except Exception as _ex:
        logger.error(f'[INFO]: GENERAL EXCEPTION DURING RUNTIME - {_ex}')
    finally:
        await storage.close()
        logger.info('[INFO]: THE BOT SESSION HAS SUCCESSFULLY BEEN CLOSED!')


def start_bot() -> None:
    """Restarts runtime process when it needs to be
    """
    print('123')
    try:
        asyncio.run(main(bot))
    except (KeyboardInterrupt, SystemExit):
        print('The bot session has been closed!')


if __name__ == "__main__":
    reloader = hupper.start_reloader('main.start_bot')
    start_bot()
