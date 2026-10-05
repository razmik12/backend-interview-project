from uuid import UUID
from redis.asyncio import Redis
from app.exceptions.general_exception import RateLimitExceededError
from app.schemas.general import Prefix
import uuid

class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    def _key(self, id: UUID, prefix: Prefix) -> str:
        return f"{prefix.value}:{id}"

    async def set(
        self,
        id: UUID,
        prefix: Prefix,
        value: str,
        ttl: int | None = None,
    ) -> None:
        key = self._key(id=id, prefix=prefix)

        await self.redis.set(
            name=key,
            value=value,
            ex=ttl,
        )

    async def get(
        self,
        id: UUID,
        prefix: Prefix,
    ) -> str | None:
        key = self._key(id=id, prefix=prefix)

        return await self.redis.get(name=key)

    async def delete(
        self,
        id: UUID,
        prefix: Prefix,
    ) -> None:
        key = self._key(id=id, prefix=prefix)

        await self.redis.delete(key)

    async def rate_limiting(
        self,
        ttl: int,
        limit: int,
        identifier:str
    ) -> int:
        key =  f"{Prefix.RATE_LIMIT.value}:{identifier}"

        count = await self.redis.incr(name=key)

        if count == 1:
            await self.redis.expire(
                name=key,
                time=ttl,
            )

        if count > limit:
            raise RateLimitExceededError()

        return count
    
    async def acquire_lock(
        self,
        session_id:UUID,
        ttl:int | None
    )->str|None:
        token = str(uuid.uuid4())
        key = self._key(id=session_id,prefix=Prefix.LOCK)
        
        acquired = await self.redis.set(key,token,nx=True,ex=ttl)
        
        return token if acquired else None
    
    
    async def release_lock(self,token:str,session_id:UUID):
         
        key = self._key(
            id=session_id,
            prefix=Prefix.LOCK,
            )
         
        script = """
                local token = redis.call("GET", KEYS[1])
                if token == ARGV[1] then
                return redis.call("DEL", KEYS[1])
            end

            return 0
"""
        result = await self.redis.eval(script,1,key,token)
         
        return result
        