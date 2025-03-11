from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn
from universal_controller import UniversalController

# Initialize the Universal Controller
controller = UniversalController()

# Define the request handler
async def handle_request(request):
    # Parse the YAML request
    yaml_request = await request.body()
    
    # Process the request
    result = controller.process_request(yaml_request)
    
    # Return the result as JSON
    return JSONResponse(result)

# Define the routes
routes = [
    Route("/process", handle_request, methods=["POST"])
]

# Create the Starlette app
app = Starlette(routes=routes)

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)