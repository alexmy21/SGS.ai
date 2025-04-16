import importlib.util
import sys
import yaml

class Controller:
    def __init__(self):
        self.processors = {}

    def load_processor(self, processor_name):
        """
        Dynamically load a processor based on its name.
        """
        try:
            # Split the processor name into module and function/class
            module_name, func_name = processor_name.rsplit(".", 1)
            
            # Dynamically import the module
            module = importlib.import_module(module_name)

            # Dynamically load the function
            processor_func = getattr(module, func_name, None)
            # Check if the function is callable
            if not callable(processor_func):
                raise TypeError(f"Processor '{processor_name}' is not callable")
            
            # Check if the function is None
            if processor_func is None:
                raise AttributeError(f"Processor '{processor_name}' could not be loaded")

            # Call the processor function
            return processor_func()
            
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Processor '{processor_name}' could not be loaded: {e}")

    
    def process_request(self, yaml_request):
        # Parse the YAML request
        request = yaml.safe_load(yaml_request)
        
        # Get the processor name
        processor_name = request.get("processor")

        print(f"Processor name: {processor_name}")

        if not processor_name:
            return {"status": "error", "message": "Processor name not provided"}
        
        # Load the processor dynamically if not already loaded        
        try:
            # processor = 
            return self.load_processor(processor_name)
            # return processor()
        except ImportError as e:
            return {"status": "error", "message": str(e)}
        