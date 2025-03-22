# Use a lightweight Python image
FROM python:3.12-slim

# Install system dependencies for Julia
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    libunwind-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Julia
ENV JULIA_VERSION=1.9.3
RUN wget https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-${JULIA_VERSION}-linux-x86_64.tar.gz \
    && tar -xvzf julia-${JULIA_VERSION}-linux-x86_64.tar.gz -C /usr/local --strip-components=1 \
    && rm julia-${JULIA_VERSION}-linux-x86_64.tar.gz

# Add Julia to PATH
ENV PATH="/usr/local/bin:$PATH"

# Install uv
RUN python -m pip install uv

# Set the working directory
#==============================================================================
WORKDIR /app

# Debug: List the contents of the build context
RUN ls -l /app

# Copy the HllSets directory to the working directory
COPY sgs_core/HllSets /app/HllSets

# Install HllSets as a Julia package
RUN julia -e 'using Pkg; Pkg.develop(path="/app/HllSets")'
#==============================================================================

# Copy the SGS.core source code
COPY sgs_core/*.py .

# Copy pyproject.toml
COPY pyproject.toml .

# Install the pyproject file
RUN uv pip install -r pyproject.toml --all-extras --system

RUN python boot_julia.py

# Expose the server port
EXPOSE 8000

# Start the SGS.core server
CMD ["python", "core_server.py"]