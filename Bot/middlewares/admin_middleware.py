import logging

from aiogram import types
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Awaitable, Dict, Any, Coroutine



class AdminOnlyMiddleware(BaseMiddleware):
    """Middleware for admin_router. Regulates admin's commands and updates properly"""

    ADMIN_LIST = {'6018428620', '973459911'}    # O(1)

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]) -> Coroutine[Any, Any, Any]:
        user_id = str(event.from_user.id)
        if isinstance(event, types.Message) and not event.text.startswith('/'):
            # Пропускаем текстовые сообщения
            return await handler(event, data)
        if user_id not in self.ADMIN_LIST and isinstance(event, types.Message) and event.text.startswith('/'):
            logging.info(f'ADMIN NOT PASSED - {user_id}')
            await event.answer('У вас нет доступа к этой команде!')
            return

        return await handler(event, data)
