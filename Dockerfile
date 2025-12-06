# Use an official Python runtime as a parent image
FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy the project files
COPY pyproject.toml uv.lock ./

# Install dependencies
# --frozen ensures we use the exact versions in uv.lock
RUN uv sync --frozen

# Copy the rest of the application code
COPY src/ src/
COPY rules.json .
COPY README.md .
COPY README_CN.md .

# Define the command to run the application
# Using `uv run` to ensure we use the virtual environment created by uv
ENTRYPOINT ["uv", "run", "python", "-m", "src.main"]
