import redis
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import numpy as np
from meta_algebra import HllSet

class RedisStore:
    def __init__(self, host='redis', port=6379, db=0):
        """
        Initialize a connection to Redis.
        
        Args:
            host: Redis host (default 'redis')
            port: Redis port (default 6379)
            db: Redis database number (default 0)
        """
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            socket_connect_timeout=5,  # 5 second timeout
            decode_responses=False  # Keep binary data intact
        )

        try:
            self._create_indices()
            print("Redisearch indices created successfully.")
        except redis.exceptions.ResponseError as e:
            if "Index already exists" in str(e):
                print("Indices already exist.")
            else:
                print(f"Error creating indices: {e}")
        except redis.exceptions.ConnectionError:
            print("Could not connect to Redis")
        except redis.exceptions.TimeoutError:
            print("Redis connection timed out")        
        except redis.exceptions.RedisError as e:
            print(f"Redis error: {e}")

    def _create_indices(self):
        """Initialize Redisearch indices."""
        # Edges Index (left_hll → right_hll)
        self.redis.ft("edges").create_index([
            TextField("e_sha1"),
            TextField("label"),
            TextField("left"),
            TextField("right"),
            TextField("attr")
        ], definition=IndexDefinition(prefix=["meta:edges:"]))

        # Tokens Index (token → data_ids)
        self.redis.ft("tokens").create_index([
            TextField("hash"),
            NumericField("bin"),
            NumericField("zeros"),
            NumericField("TF"),
            TagField("refs")
        ], definition=IndexDefinition(prefix=["meta:tokens:"]))

        # Commits Index (commit → timestamp)
        self.redis.ft("commits").create_index([
            TextField("c_sha1"),
            NumericField("timestamp")
        ], definition=IndexDefinition(prefix=["meta:commits:"]))    

    
    def execute_graph_query(self, query):
        """Execute a Redis Graph query."""
        return self.redis.execute_command("GRAPH.QUERY", "graph", query)

    def roaring_bitmap_command(self, command, *args):
        """Execute a Redis Roaring Bitmap command."""
        return self.redis.execute_command(command, *args)

    def search(self, index_name, query):
        """Search a Redisearch index."""
        return self.redisearch_client.search(query)

    def ping(self, **kwargs):
        """
        Test Redis connection with configurable parameters.
        
        Args:
            kwargs: Can include 'test_key' and 'test_value' for verification
        Returns:
            dict: Status and response information
        """
        try:
            test_key = kwargs.get('test_key', 'sgs:ping_test')
            test_value = kwargs.get('test_value', b'pong')
            
            # Test write/read cycle
            self.redis.set(test_key, test_value)
            retrieved = self.redis.get(test_key)
            
            return {
                "status": "success",
                "response": retrieved == test_value,
                "latency": self.redis.latency_latest()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "type": type(e).__name__
            }

    def store_hllset(self, key: str, hllset: HllSet, **kwargs):
        """
        Store an HllSet in Redis with additional options.
        
        Args:
            key: Redis key to store under
            hllset: HllSet object to store
            kwargs: Additional Redis set() options like:
                   ex (expire in seconds), px (expire in ms)
        """
        try:
            counts = hllset.counts
            byte_array = counts.tobytes()
            return self.redis.set(key, byte_array, **kwargs)
        except Exception as e:
            raise ValueError(f"Failed to store HllSet: {str(e)}")

    def retrieve_hllset(self, key: str, P: int = 10) -> HllSet:
        """
        Retrieve an HllSet from Redis.
        
        Args:
            key: Redis key to retrieve
            P: Precision for new HllSet (default 10)
        Returns:
            HllSet or None if key doesn't exist
        """
        try:
            byte_array = self.redis.get(key)
            if byte_array is None:
                return None
                
            counts = np.frombuffer(byte_array, dtype=np.uint32)
            hllset = HllSet(P)
            hllset.counts = counts
            return hllset
        except Exception as e:
            raise ValueError(f"Failed to retrieve HllSet: {str(e)}")

    def set_operation(self, operation: str, keys: list, result_key: str, **kwargs):
        """
        Perform set operations on HllSets stored in Redis.
        
        Args:
            operation: One of ['union', 'intersection', 'difference']
            keys: List of source keys (2 required)
            result_key: Key to store result under
            kwargs: Additional storage options
        """
        if len(keys) != 2:
            raise ValueError("Exactly 2 keys required for set operations")
            
        ops = {
            'union': lambda a, b: a.union(b),
            'intersection': lambda a, b: a.intersection(b),
            'difference': lambda a, b: a.diff(b)
        }
        
        if operation not in ops:
            raise ValueError(f"Invalid operation. Must be one of {list(ops.keys())}")
            
        hll1 = self.retrieve_hllset(keys[0])
        hll2 = self.retrieve_hllset(keys[1])
        
        if hll1 is None or hll2 is None:
            raise ValueError("One or both HllSets not found")
            
        result = ops[operation](hll1, hll2)
        return self.store_hllset(result_key, result, **kwargs)

# Standalone function for compatibility
def ping_redis(**kwargs):
    """
    Standalone function to ping Redis.
    Compatible with dynamic calling system.
    """
    store = RedisStore()
    return store.ping(**kwargs)