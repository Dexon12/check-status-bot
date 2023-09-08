from datetime import timedelta, datetime, time
import asyncio

from Bot.DataBase.db import UserService
from Bot.keyboards.ikb import do_you_work_today
from bot_instance import bot
from Bot.DataBase.redis_db import UserRedisService
from Bot.utils.logger import setup_logger
logger = setup_logger('main_logger', 'main_logs.log')


def delay_time():
    eleven = None

    def time_until_eleven():
        now = datetime.now()
        nonlocal eleven

        if eleven is None:
            eleven = datetime.combine(now.date(), time(hour=19, minute=5))
        if now > eleven:
            eleven += timedelta(minutes=1)
            print(eleven)

        difference = abs(eleven - now)
        return difference.total_seconds()
    return time_until_eleven


delay_test = delay_time()


async def send_msg():
    all_id = set(await UserService.select_users_id())

    while True:
        delay = delay_test()
        print(2, delay)
        await asyncio.sleep(delay)
        await UserRedisService.delete_users_answer()
        logger.info('[INFO]: sending_msg is active!')
        for ids in all_id:
            is_subscribed = await UserService.take_subscribe(int(ids))
            if is_subscribed:  # Получаем актуальное значение задержки перед каждой отправкой сообщения
                await bot.send_message(chat_id=int(ids), text='Работаешь сегодня?', reply_markup=do_you_work_today())
            else:
                continue  # Пропускаем отправку сообщения и переходим к следующему пользователю
        