import asyncio

from env_loader import EnvLoader
from redis_client import RedisClient


async def main() -> None:
    """
    Example usage of EnvLoader and RedisClient.
    """
    config = EnvLoader(".env")

    print(f"App Name: {config.APP_NAME}")
    print(f"Secret Key: {config.SECRET_KEY}")

    async with RedisClient(config.REDIS_URL) as redis:
        # Strings
        await redis.set("greeting", "hello", ttl=60)
        value = await redis.get("greeting")
        print(f"String get: {value}")

        # Hashes
        await redis.hset("user:1", {"name": "Alice", "role": "admin"})
        user = await redis.hgetall("user:1")
        print(f"Hash hgetall: {user}")

        # Lists
        await redis.lpush("queue", "task1", "task2", "task3")
        items = await redis.lrange("queue", 0, -1)
        print(f"List lrange: {items}")

        # Sets
        await redis.sadd("tags", "python", "redis", "async")
        tags = await redis.smembers("tags")
        print(f"Set smembers: {tags}")

        # Pub/Sub — publish only (subscribe requires a background task)
        receivers = await redis.publish("news", "Redis is awesome!")
        print(f"Publish receivers: {receivers}")
        # To subscribe: async for msg in redis.subscribe("news"): ...


# python3 main.py
if __name__ == "__main__":
    asyncio.run(main())
