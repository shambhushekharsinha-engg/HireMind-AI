import time
from collections import defaultdict
from typing import Dict, List

from fastapi import HTTPException, Request


class SimpleRateLimiter:
    """
    In-memory Token Bucket / Sliding Window Rate Limiter.
    Limits key endpoints like /login, /coach, /resumes/upload per IP address.
    """

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def check_rate_limit(self, request: Request, custom_limit: int = None):
        limit = custom_limit or self.requests_per_minute
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        # Clean timestamps older than 60 seconds
        self.requests[client_ip] = [ts for ts in self.requests[client_ip] if now - ts < 60]

        if len(self.requests[client_ip]) >= limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please wait before retrying.")

        self.requests[client_ip].append(now)


rate_limiter = SimpleRateLimiter()
