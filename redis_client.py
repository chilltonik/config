import logging
from collections.abc import AsyncGenerator
from typing import cast

import redis.asyncio as aioredis

# ───────────────────────────────────────────────────────────────
# Logger Configuration
# ───────────────────────────────────────────────────────────────

logger = logging.getLogger("redis_client")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(message)s")
)
logger.addHandler(handler)


class RedisClient:
    """
    Async Redis client supporting strings, hashes, lists, sets, and pub/sub.

    Use as an async context manager or call connect()/disconnect() manually.
    """

    def __init__(self, url: str) -> None:
        self._url = url
        self._client: aioredis.Redis[str] | None = None

    async def __aenter__(self) -> "RedisClient":
        await self.connect()
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.disconnect()

    async def connect(self) -> None:
        self._client = cast(
            "aioredis.Redis[str]",
            aioredis.from_url(self._url, decode_responses=True),
        )
        logger.info("Connected to Redis: %s", self._url)

    async def disconnect(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.info("Redis connection closed")

    def _require_client(self) -> "aioredis.Redis[str]":
        if self._client is None:
            raise RuntimeError(
                "Redis client is not connected. Call connect() first."
            )
        return self._client

    # ── Strings ─────────────────────────────────────────────────

    async def get(self, key: str) -> str | None:
        return cast("str | None", await self._require_client().get(key))

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        await self._require_client().set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        await self._require_client().delete(key)

    # ── Hashes ──────────────────────────────────────────────────

    async def hset(self, name: str, mapping: dict[str, str]) -> None:
        await self._require_client().hset(name, mapping=mapping)

    async def hget(self, name: str, key: str) -> str | None:
        return cast("str | None", await self._require_client().hget(name, key))

    async def hgetall(self, name: str) -> dict[str, str]:
        return cast(
            "dict[str, str]", await self._require_client().hgetall(name)
        )

    async def hdel(self, name: str, *keys: str) -> None:
        await self._require_client().hdel(name, *keys)

    # ── Lists ────────────────────────────────────────────────────

    async def lpush(self, key: str, *values: str) -> None:
        await self._require_client().lpush(key, *values)

    async def rpush(self, key: str, *values: str) -> None:
        await self._require_client().rpush(key, *values)

    async def lpop(self, key: str) -> str | None:
        return cast("str | None", await self._require_client().lpop(key))

    async def rpop(self, key: str) -> str | None:
        return cast("str | None", await self._require_client().rpop(key))

    async def lrange(self, key: str, start: int, end: int) -> list[str]:
        return cast(
            "list[str]", await self._require_client().lrange(key, start, end)
        )

    # ── Sets ─────────────────────────────────────────────────────

    async def sadd(self, key: str, *members: str) -> None:
        await self._require_client().sadd(key, *members)

    async def smembers(self, key: str) -> set[str]:  # type: ignore[valid-type]
        return cast("set[str]", await self._require_client().smembers(key))

    async def srem(self, key: str, *members: str) -> None:
        await self._require_client().srem(key, *members)

    async def sismember(self, key: str, member: str) -> bool:
        return bool(await self._require_client().sismember(key, member))

    # ── Pub/Sub ──────────────────────────────────────────────────

    async def publish(self, channel: str, message: str) -> int:
        return cast(
            "int", await self._require_client().publish(channel, message)
        )

    async def subscribe(
        self, *channels: str
    ) -> AsyncGenerator[dict[str, str], None]:
        pubsub = self._require_client().pubsub()
        await pubsub.subscribe(*channels)
        try:
            async for raw in pubsub.listen():
                if raw["type"] == "message":
                    yield {
                        "channel": str(raw["channel"]),
                        "data": str(raw["data"]),
                    }
        finally:
            await pubsub.unsubscribe(*channels)
            await pubsub.aclose()
