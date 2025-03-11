# import redis
import yaml
from ping_redis import ping_redis


class UniversalController:
    def __init__(self):
        self.processors = {
            "ping_redis": ping_redis
        }

    def process_request(self, yaml_request):
        # Parse the YAML request
        request = yaml.safe_load(yaml_request)
        
        # Get the processor
        processor_name = request.get("processor")
        if processor_name not in self.processors:
            return {"status": "error", "message": "Processor not found"}
        
        # Execute the processor
        processor = self.processors[processor_name]
        result = processor()
        
        return result