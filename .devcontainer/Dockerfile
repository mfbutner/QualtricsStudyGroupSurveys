FROM ubuntu:rolling

# Install stuff like git,pip,and pipx
RUN apt-get update && apt-get install -y \
    sudo \
    git \
    python3-pip \
    python3-venv \
    pipx \
    && rm -rf /var/lib/apt/list

# Create a non-root user
RUN useradd -m -s /bin/bash pythondev && \
    usermod -aG sudo pythondev && \
    echo "pythondev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set up workspace
RUN mkdir -p /home/pythondev/qualtrics && \
    chown -R pythondev:pythondev /home/pythondev

# Switch to non-root user
USER pythondev

# Initialize pipx for the user
RUN pipx ensurepath

# Install devtool
RUN pipx install \
    ruff \
    uv