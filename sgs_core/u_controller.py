# import redis
import yaml
from meta_redis import RedisStore as r_store
from meta_hdf5 import HDF5Store as h_store

class Controller:
    def __init__(self):
        self.processors = {
            "ping_redis": r_store.ping_redis,
            "call_hdf5": h_store.call_hdf5
        }

    def process_request(self, yaml_request):
        # Parse the YAML request
        request = yaml.safe_load(yaml_request)
        
        # Get the processor
        processor_name = request.get("processor")
        if processor_name not in self.processors:
            return {"status": "error", "message": "Processor not found"}
        
        # Execute the processor
        try:
            processor = self.processors[processor_name]
            result = processor()
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}