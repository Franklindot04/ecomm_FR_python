from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.redis_client import redis_client


async def rate_limit_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    client_ip = request.client.host if request.client else "unknown"
    username = form_data.username.strip().lower()
    key = f"rate_limit:login:{client_ip}:{username}"

    current = await redis_client.incr(key)

    if current == 1:
        await redis_client.expire(key, settings.rate_limit_seconds)

    if current > settings.rate_limit_times:
        ttl = await redis_client.ttl(key)

        if ttl < 0:
            ttl = settings.rate_limit_seconds

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts for '{username}'. Try again in {ttl} seconds.",
            headers={"Retry-After": str(ttl)},
        )
