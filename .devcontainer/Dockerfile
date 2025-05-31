# Azure Terraform Modules Development Container
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        build-essential \
        curl \
        git \
        jq \
        unzip \
        wget \
        ca-certificates \
        gnupg \
        lsb-release \
        software-properties-common \
    && apt-get autoremove -y && apt-get clean -y

# Install Poetry
RUN pip install poetry==1.8.3 \
    && poetry config virtualenvs.create false

# Install additional security tools that might not be in Poetry
RUN pip install \
    safety \
    bandit[toml] \
    checkov

# Install terraform-docs
RUN curl -sSLo terraform-docs.tar.gz https://terraform-docs.io/dl/v0.17.0/terraform-docs-v0.17.0-linux-amd64.tar.gz \
    && tar -xzf terraform-docs.tar.gz \
    && chmod +x terraform-docs \
    && mv terraform-docs /usr/local/bin/ \
    && rm terraform-docs.tar.gz

# Install tflint (Terraform linter)
RUN curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# Install pre-commit
RUN pip install pre-commit

# Create workspace directory
WORKDIR /workspace

# Switch to vscode user
USER vscode

# Set up shell aliases and improvements
RUN echo 'alias ll="ls -la"' >> ~/.zshrc \
    && echo 'alias la="ls -la"' >> ~/.zshrc \
    && echo 'alias ..="cd .."' >> ~/.zshrc \
    && echo 'alias ...="cd ../.."' >> ~/.zshrc \
    && echo 'alias tf="terraform"' >> ~/.zshrc \
    && echo 'alias mk="make"' >> ~/.zshrc \
    && echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Set default shell
SHELL ["/bin/zsh", "-c"]
