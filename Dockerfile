# Stage 1: Build environment
FROM python:3.12-slim AS build

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

# Set the HLLSETS_PATH environment variable
ENV HLLSETS_PATH=/app/HllSets/src/HllSets.jl

# Install uv
RUN python -m pip install uv

# Set the working directory
WORKDIR /app

# Copy the HllSets directory to the working directory
COPY sgs_core/HllSets /app/HllSets

# Install HllSets as a Julia package
RUN julia -e 'using Pkg; Pkg.develop(path="/app/HllSets")'

# Copy pyproject.toml
COPY pyproject.toml .

# Install Python dependencies
RUN uv pip install -r pyproject.toml --all-extras --system

# Copy the rest of the application code
COPY sgs_core/*.py .

# Run boot_julia.py during the build
RUN python boot_julia.py

# Set the working directory
WORKDIR /app

# Expose the server port
EXPOSE 8000

# Add a health check
HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the SGS.core server
ENTRYPOINT ["python"]
CMD ["core_server.py"]