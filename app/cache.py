import time

cache_store = {}

CACHE_TTL = 3600  # 60 minutes (in seconds)

def get_from_cache(key: str):
    if key in cache_store:
        data, timestamp = cache_store[key]

        #  check expiry
        if time.time() - timestamp < CACHE_TTL:
            return data
        else:
            del cache_store[key]  # remove expired

    return None


def save_to_cache(key: str, value):
    cache_store[key] = (value, time.time())