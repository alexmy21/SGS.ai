# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy the requirements file
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install -r pyproject.toml

# Copy the SGS.core source code
COPY . .

# Expose the server port
EXPOSE 8000

# Start the SGS.core server
CMD ["uvicorn", "core_server:app", "--host", "0.0.0.0", "--port", "8000"]