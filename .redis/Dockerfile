# Use Redis 7.0.15 as the base image
FROM redis:7.0.15
RUN apt-get update && apt-get install -y libgomp1

# Set the working directory
WORKDIR /usr/local/lib/redis

# Copy Redis modules and configuration
COPY .redis/libredis-roaring.so .
COPY .redis/redisearch.so .
COPY .redis/redisgraph.so .
COPY .redis/redis.conf /usr/local/etc/redis/redis.conf

# Copy the Lua library
COPY ../src/hll_algebra.lua /usr/local/lib/redis/hll_algebra.lua

# Expose the Redis port
EXPOSE 6379

# Start Redis with the custom configuration
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]