# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the wheel file
COPY dist/sgs_ai-0.1.0-py3-none-any.whl .

# Install the wheel file
RUN pip install sgs_ai-0.1.0-py3-none-any.whl

# Copy the SGS.core source code
COPY . .

# Expose the server port
EXPOSE 8000

# Start the SGS.core server
CMD ["python", "sgs_core/core_server.py"]