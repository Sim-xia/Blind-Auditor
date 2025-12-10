# Use official Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Set the working directory in the container
WORKDIR /app

# Copy project files for dependency installation
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application code
COPY src/ src/
COPY rules.json .
COPY README.md .
COPY README_CN.md .

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Define the command to run the application
ENTRYPOINT ["uv", "run", "blind-auditor"]
