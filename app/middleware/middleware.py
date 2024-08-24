import logging
import time
from typing import Optional

from aioredis import Redis, from_url
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("Application")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str, rate_limit: int, rate_limit_period: int):
        super().__init__(app)
        self.redis_url = redis_url
        self.rate_limit = rate_limit
        self.rate_limit_period = rate_limit_period
        self.redis: Optional[Redis] = None

    async def dispatch(self, request: Request, call_next):
        if not self.redis:
            self.redis = await from_url(self.redis_url, decode_responses=True)

        ip = request.client.host
        key = f"ratelimit:{ip}"

        current_time = int(time.time())
        start_time = current_time - self.rate_limit_period

        try:
            logger.info(f"Handling Request From IP: {ip} At Time: {current_time}!!!")

            removed = await self.redis.zremrangebyscore(key, 0, start_time)
            logger.info(f"Removed {removed} Outdated Requests for Key: {key}!!!")

            request_count = await self.redis.zcard(key)
            logger.info(f"Current Request Count For Key {key}: {request_count}!!!")

            if request_count >= self.rate_limit:
                logger.warning(f"Rate Limit Exceeded For Key {key}!!!")
                raise HTTPException(
                    status_code=429,
                    detail="Too Many Requests From This IP. Please Try Again Later!!!"
                )

            logger.info(f"Added Request At Time {current_time} For Key {key}!!!")

            expiration_set = await self.redis.expire(key, self.rate_limit_period)
            logger.info(f"Set Expiration For Key {key}: {expiration_set}!!!")

            response = await call_next(request)
            logger.info(f"Request Handled Successfully for IP: {ip}!")
            return response

        except Exception as e:
            logger.error(f"Error In RateLimitMiddleware: {e}!!!", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error"
            )
