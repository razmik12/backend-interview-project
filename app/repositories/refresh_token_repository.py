from uuid import UUID

from redis.asyncio import Redis


class RefreshTokenRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    def _get_key(self, session_id: UUID, user_id: UUID) -> str:
        return f"key:{user_id}:{session_id}"

    async def set_token(
        self, token: str, user_id: UUID, session_id: UUID, ttl: int
    ) -> None:
        key = self._get_key(session_id=session_id, user_id=user_id)
        await self.redis.set(name=key, value=token, ex=ttl)

    async def get_token(self, user_id: UUID, session_id: UUID) -> str | None:
        key = self._get_key(session_id=session_id, user_id=user_id)
        token = await self.redis.get(name=key)
        if isinstance(token, bytes):
            return token.decode("utf-8")
        return token

    async def delete_token(self, user_id: UUID, session_id: UUID) -> bool:
        key = self._get_key(session_id=session_id, user_id=user_id)
        deleted = await self.redis.delete(key)
        return deleted == 1
