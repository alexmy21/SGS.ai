"""ID Management and Indexing System for HLL Metadata."""

import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
import redis
from redis.commands.search.field import TextField, TagField
from redis.commands.search.indexDefinition import IndexDefinition

@dataclass
class HllIdentifier:
    data_id: str  # SHA1 of data location (stable)
    hll_id: str   # SHA1 of HLL content (changes)
    timestamp: float

class MetadataIndexer:
    def __init__(self, redis_conn: redis.Redis):
        self.redis = redis_conn
        self._create_indices()

    def _create_indices(self):
        """Initialize Redisearch indices."""
        # Provenance Index (data_id → hll_ids)
        self.redis.ft("provenance_idx").create_index([
            TagField("data_id"),
            TextField("hll_ids"),
            TextField("timestamps")
        ], definition=IndexDefinition(prefix=["meta:provenance:"]))

        # Inverted Index (token → data_ids)
        self.redis.ft("inverted_idx").create_index([
            TextField("token"),
            TagField("data_ids")
        ], definition=IndexDefinition(prefix=["meta:inverted:"]))
    
    def record_hllset(self, data_location: str, hll_bytes: bytes) -> HllIdentifier:
        """Record a new HLL set with provenance."""
        data_id = self._sha1(data_location.encode())
        hll_id = self._sha1(hll_bytes)
        
        # Store in provenance index
        prov_key = f"meta:provenance:{data_id}"
        self.redis.hset(prov_key, mapping={
            "data_id": data_id,
            "hll_ids": self.redis.hget(prov_key, "hll_ids") or "" + f"{hll_id},",
            "timestamps": self.redis.hget(prov_key, "timestamps") or "" + f"{time.time()},",
        })
        
        return HllIdentifier(data_id, hll_id, time.time())

    def index_tokens(self, data_id: str, tokens: List[str]):
        """Update inverted index with tokens from data."""
        for token in tokens:
            inv_key = f"meta:inverted:{token}"
            self.redis.sadd(inv_key, data_id)

    def get_data_versions(self, data_id: str) -> List[HllIdentifier]:
        """Get all HLL versions for a data source."""
        prov_key = f"meta:provenance:{data_id}"
        hll_ids = self.redis.hget(prov_key, "hll_ids").split(",")
        timestamps = self.redis.hget(prov_key, "timestamps").split(",")
        
        return [
            HllIdentifier(data_id, hll_id, float(ts))
            for hll_id, ts in zip(hll_ids, timestamps)
            if hll_id
        ]

    def lookup_token(self, token: str) -> List[str]:
        """Find data_ids containing a token."""
        return list(self.redis.smembers(f"meta:inverted:{token}"))

    @staticmethod
    def _sha1(data: bytes) -> str:
        return hashlib.sha1(data).hexdigest()