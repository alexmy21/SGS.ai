import redis

def ping_redis():
    # Connect to Redis
    r = redis.Redis(host="localhost", port=6379)
    
    # Ping Redis
    response = r.ping()
    
    # Return the response
    return {"status": "success", "response": response}
