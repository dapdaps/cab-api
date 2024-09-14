import logging
import json
import uuid
import time

import redis

from core.utils.json_utils import JsonEncoder
from settings.config import settings

logger = logging.getLogger(__name__)

if settings.REDIS_PASSWORD:
    pool = redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        connection_class=redis.SSLConnection if settings.REDIS_USE_TLS else redis.Connection,
        decode_responses=True
    )
else:
    pool = redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
        db=settings.REDIS_DB,
        decode_responses=True
    )
normal_lock_prefix = "lock:"


def get_client():
    return redis.StrictRedis(connection_pool=pool)


def release_lock(lock_key, lock_value):
    lock_key = normal_lock_prefix + lock_key
    client = get_client()
    value = client.get(lock_key)
    if value:
        if lock_value != value:
            logger.info(f"lock {lock_key} value changed before release")
        else:
            client.delete(lock_key)
    else:
        logger.info(f"lock {lock_key} not exist before release")
    client.close()


def get_lock(lock_key, expiry_seconds):
    lock_key = normal_lock_prefix+lock_key
    value = str(uuid.uuid4())
    try:
        client = get_client()
        res = client.set(lock_key, value, ex=expiry_seconds, nx=True)
        client.close()
        return res, value
    except Exception as e:
        logger.error(f"redis set Exception: {e}")
    return False, value


async def with_lock_timeout(lock_key, expiry_seconds, func):
    start_time = int(round(time.time() * 1000))
    max_time = 5000
    while True:
        lock_res, lock_value = get_lock(lock_key, expiry_seconds)
        if not lock_res and int(round(time.time() * 1000))-start_time < max_time:
            time.sleep(0.5)
            continue
        break

    if lock_res:
        try:
            await func()
        finally:
            release_lock(lock_key, lock_value)
    return lock_res


async def with_lock(lock_key, func):
    res = await with_lock_timeout(lock_key, 15, func)
    return res


def set_value(key: str, value):
    r = get_client()
    r.set(key, value)
    r.close()


def get_value(key: str):
    r = get_client()
    value = r.get(key)
    r.close()
    return value


def hget_all(name: str):
    r = get_client()
    ret = r.hgetall(name)
    r.close()
    return ret


def hset_all(name: str, map_data):
    r = get_client()
    for key, value in map_data.items():
        r.hset(name, key, value)
    r.close()


def hget(name: str, key: str):
    r = get_client()
    ret = r.hget(name, key)
    r.close()
    return ret


def hget_all_json(name: str):
    r = get_client()
    ret = r.hgetall(name)
    if ret:
        ret = {k: json.loads(v) for k, v in ret.items()}
    r.close()
    return ret


def hset_all_json(name: str, mapping_data):
    r = get_client()
    for key, value in mapping_data.items():
        r.hset(name, key, json.dumps(value, cls=JsonEncoder))
    r.close()


def hget_json(name: str, key: str):
    r = get_client()
    ret = r.hget(name, key)
    if ret:
        ret = json.loads(ret)
    r.close()
    return ret


def set_array_json(name: str, array_data):
    json_array_data = [json.dumps(item) for item in array_data]
    r = get_client()
    r.rpush(name, *json_array_data)
    r.close()


def get_array_json(name: str):
    r = get_client()
    ret = r.lrange(name, 0, -1)
    if ret and len(ret) > 0:
        ret = [json.loads(item) for item in ret]
    r.close()
    return ret


def hmget_json(name: str, keys):
    r = get_client()
    ret = r.hmget(name, *keys)
    if ret:
        ret = [json.loads(value) if value else None for value in ret]
    r.close()
    return ret


def hset_json(name: str, key: str, data):
    r = get_client()
    ret = r.hset(name, key, json.dumps(data))
    r.close()
    return ret


def hget_value(name: str, key: str, ):
    r = get_client()
    ret = r.hget(name, key)
    r.close()
    return ret


if __name__ == '__main__':
    set_value("testDapDap", "1")
