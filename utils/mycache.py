import memcache


cache = memcache.Client(['127.0.0.1:11211'],debug=True)

def set_(key,value,timeout=60):
    return cache.set(key,value,timeout)

def get_(key):
    return cache.get(key)

def delete_(key):
    return cache.delete(key)