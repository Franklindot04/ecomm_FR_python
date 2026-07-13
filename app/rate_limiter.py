import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.redis_client import redis_client

load_dotenv()

RATE_LIMIT_TIMES = int(os.getenv("RATE_LIMIT_TIMES", "5"))
RATE_LIMIT_SECONDS = int(os.getenv("RATE_LIMIT_SECONDS", "60"))


async def rate_limit_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    client_ip = request.client.host if request.client else "unknown"
    username = form_data.username.strip().lower()
    key = f"rate_limit:login:{client_ip}:{username}"

    current = await redis_client.incr(key)

    if current == 1:
        await redis_client.expire(key, RATE_LIMIT_SECONDS)

    if current > RATE_LIMIT_TIMES:
        ttl = await redis_client.ttl(key)

        if ttl < 0:
            ttl = RATE_LIMIT_SECONDS

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts for '{username}'. Try again in {ttl} seconds.",
            headers={"Retry-After": str(ttl)},
        )