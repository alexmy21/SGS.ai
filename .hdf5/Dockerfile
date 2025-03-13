# .hdf5/Dockerfile
FROM python:3.12-slim

# Install HDF5 and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    wget \
    libhdf5-dev \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy custom HDF5 configuration or scripts
WORKDIR /app

# Copy the wheel file
COPY dist/sgs_ai-0.1.0-py3-none-any.whl .

# Install the wheel file
RUN pip install sgs_ai-0.1.0-py3-none-any.whl

# Copy the SGS.core source code
COPY .hdf5/* .

# Expose the HDF5 server port (if applicable)
EXPOSE 5000

# Set the entrypoint or command
# CMD ["/bin/bash"]
CMD ["python3", "hdf5_server.py"]