import time
from functools import wraps
from fastapi import Request, status, HTTPException
from core.exception.base import TooManyRequestException
from core.connections.redis import redis_db, blacklist


def rate_limit(max_calls: int, time_frame):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host
            now = time.time()
            key = f"ratelimit:{client_ip}"
            # Get the number of calls made by the client within the time frame
            client_rate = redis_db.zcount(key, now - time_frame, now)
            if client_rate >= max_calls:
                blacklist.set(f"blacklist:{client_ip}", client_ip, ex=300)
                raise TooManyRequestException()

            # Add the current call to Redis with its timestamp
            redis_db.zadd(key, {now: now})

            # Remove old timestamps to keep the Redis set clean
            redis_db.zremrangebyscore(key, 0, now - time_frame)

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
