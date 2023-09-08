from typing import List, Tuple, Any
import os
import redis.asyncio as redis


class RedisHandler:
    """Singleton class for redis-client engine"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self, host='aiogram_3_version-redis2-1', port=6379):
        """
        Initialize a new redis handler based on a 6379 port. 
        Because the previous one is already taken by RedisStorage aiogram library
        """

        if self.__initialized:
            return
        
        self.connection = None
        self.host = host
        self.port = port
        self.__initialized = True

    async def connect(self):
        """
        Since the redis is now under Redis officially. We only should use from_url classmethod
        so as to create a connection pool. 
        
        To be precise our `self.connection` is not a connection pool or connection itself rather 
        it's client for working with redis databases.
        """

        if not self.connection:
            self.connection = await redis.Redis.from_url(f'redis://{self.host}:{self.port}')


    async def close(self):
        """
        We should close our connection pool if it exists in our program so as to prevent memory leaks.
        """
        
        if self.connection:
            self.connection.close(close_connection_pool=True)
            
    
    @classmethod
    def get_connection(cls):
        return cls._instance.connection


class UserRedisService:

    @classmethod
    async def user_answer_rdb(cls, user_id, answer: str) -> None:
        """Starts the quiz model in redis. Attempts the number of attmpts user took for the specific question"""

        try:
            print('Before')
            connection = RedisHandler.get_connection()
            print(f"Connecting to Redis with connection: {connection}")

            r = connection
            users = 'users'
            print('After')
            print(r)
            
            async with r.pipeline(transaction=True) as pipe:   # answer - 0 or 1
                await (pipe.hset(users, user_id, answer).execute())
                
        except Exception as e:
            print(f"Exception occurred: {e}")
            raise

    @classmethod
    async def get_user_answer_rdb(cls) -> list[tuple[Any, Any]]:
        """Starts the quiz model in redis. Attempts the number of attmpts user took for the specific question"""

        connection = RedisHandler.get_connection()

        r = connection

        users = 'users'

        print(r)


        result_bytes = await r.hgetall(users)
        result = [(key.decode(), value.decode()) for key, value in result_bytes.items()]
        return result

    @classmethod
    async def delete_users_answer(cls) -> None:
        connection = RedisHandler.get_connection()

        r = connection

        await r.delete('users')   
# Что такое optimistic locking?
# decode_responses=True переводит bytes в str, в redis основной тип данных это bytes
