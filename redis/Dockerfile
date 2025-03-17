FROM redis:7.0.15
RUN apt-get update && apt-get install -y libgomp1
WORKDIR /usr/local/lib/redis
COPY libredis-roaring.so .
COPY redisearch.so .
COPY redisgraph.so .
COPY redis.conf /usr/local/etc/redis/redis.conf
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]