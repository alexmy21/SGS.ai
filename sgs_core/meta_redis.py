# meta_store.py

import redis
import numpy as np
from meta_algebra import HllSet

    
def __init__(self, host='redis', port=6379, db=0):
    """
    Initialize a connection to the Redis container.
    """
    self.redis = redis.Redis(host=host, port=port, db=db)

def ping_redis():
    # Connect to Redis
    r = redis.Redis(host="redis", port=6379)
    
    # Ping Redis
    response = r.set("foo", "bar") #r.ping()

    # Return the response
    return {"status": "success", "response": response}

def store_hllset(self, key, hllset):
    """
    Store an HllSet in Redis.
    """
    # Convert HllSet counts to a byte array
    counts = hllset.hll.counts
    byte_array = counts.tobytes()
    self.redis.set(key, byte_array)

def retrieve_hllset(self, key, P=10):
    """
    Retrieve an HllSet from Redis.
    """
    # Retrieve byte array from Redis
    byte_array = self.redis.get(key)
    if byte_array is None:
        return None
    # Convert byte array to Julia HllSet
    counts = np.frombuffer(byte_array, dtype=np.uint32)
    from meta_algebra import HllSet as JuliaHllSet
    julia_hll = JuliaHllSet(P)
    julia_hll.counts = counts
    return HllSet.from_julia(julia_hll)

def redis_union(self, key1, key2, result_key):
    """
    Perform a union of two HllSets stored in Redis and store the result.
    """
    hll1 = self.retrieve_hllset(key1)
    hll2 = self.retrieve_hllset(key2)
    if hll1 is None or hll2 is None:
        raise ValueError("One or both HllSets not found in Redis")
    result = hll1.union(hll2)
    self.store_hllset(result_key, result)

def redis_intersection(self, key1, key2, result_key):
    """
    Perform an intersection of two HllSets stored in Redis and store the result.
    """
    hll1 = self.retrieve_hllset(key1)
    hll2 = self.retrieve_hllset(key2)
    if hll1 is None or hll2 is None:
        raise ValueError("One or both HllSets not found in Redis")
    result = hll1.intersection(hll2)
    self.store_hllset(result_key, result)