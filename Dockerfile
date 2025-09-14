# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy the project configuration into the container
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-cache

# Expose the port the app runs on
EXPOSE 8080

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["uv", "run", "run.py", "-db", "-prod"]