import os
import redis
from dotenv import load_dotenv

load_dotenv()


redis_db = redis.Redis(
    host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True, db=0
)
whitelist = redis.Redis(
    host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True, db=1
)
blacklist = redis.Redis(
    host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True, db=2
)
limiter = redis.Redis(
    host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True, db=3
)
