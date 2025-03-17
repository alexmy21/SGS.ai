import redis

def ping_redis():
    # Connect to Redis
    r = redis.Redis(host="redis", port=6379)
    
    # Ping Redis
    response = r.set("foo", "bar") #r.ping()
    
    # Return the response
    return {"status": "success", "response": response}
