# Use Python 3.10 slim base image
FROM python:3.10-slim

# Install uv for fast package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY  requirements.txt ./

# Install dependencies using uv
RUN uv pip install -r requirements.txt --system

# Copy the rest of the application code
COPY . .

# Expose the port for the MCP server (default 8000)
EXPOSE 8000

# Command to run the server
CMD ["python", "server.py"]
