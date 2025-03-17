# Use a lightweight Python image
FROM python:3.12-slim

# Install uv
RUN python -m pip install uv

# Set the working directory
WORKDIR /app

# Copy the SGS.core source code
COPY sgs_core/*.py .

# Copy pyproject.toml
COPY pyproject.toml .

# Install the wheel file
RUN uv pip install -r pyproject.toml --all-extras --system

# Expose the server port
EXPOSE 8000

# Start the SGS.core server
CMD ["python", "core_server.py"]