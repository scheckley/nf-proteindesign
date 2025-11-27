# 1. Use the Runtime image (Approx. 4GB vs 9GB for devel)
# This includes PyTorch 2.3 + CUDA 12.1 drivers but NO compiler (nvcc).
FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

# Set flags to keep things clean and non-interactive
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 2. Install minimal system tools
# We need git for the install, wget for mmseqs2, and build-essential/cmake 
# temporarily in case 'dm-tree' or other deps need to compile C++ extensions.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    tar \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Python Dependencies
# We manually install PyG dependencies from wheels to avoid needing the full CUDA compiler.
# Note: The URL matches the PyTorch (2.3.0) and CUDA (12.1) versions of the base image.
RUN pip install --upgrade pip && \
    pip install torch-scatter torch-sparse torch-cluster torch-spline-conv \
    -f https://data.pyg.org/whl/torch-2.3.0+cu121.html

# 4. Install Boltz
# We install 'rdkit' specifically to ensure the pip-optimized version is used.
RUN pip install "rdkit>=2022.9.5" && \
    pip install "boltz[cuda]"

# 5. Cleanup to save space
# Remove build tools that are no longer needed for running the model.
RUN apt-get purge -y build-essential cmake && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Setup working directory
WORKDIR /app