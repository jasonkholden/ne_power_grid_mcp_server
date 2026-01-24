# MCP Server for ISO New England Power Grid Data
# Runs with HTTP transport for remote access

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY run_http_server.py .

# Expose HTTP port
EXPOSE 8080

# Run the HTTP server
CMD ["python", "run_http_server.py"]
