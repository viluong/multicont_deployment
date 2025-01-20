from redis.asyncio import Redis
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))

def fib(index):
    if index < 2:
        return 1
    return fib(index - 1) + fib(index - 2)


async def main():
    redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)

    sub = redis_client.pubsub()

    await sub.subscribe("insert")

    while True:
        message = await sub.get_message(ignore_subscribe_messages=True)
        if message:
            index = int(message["data"])
            await redis_client.hset("values", str(index), fib(index))

if __name__ == "__main__":
    asyncio.run(main())