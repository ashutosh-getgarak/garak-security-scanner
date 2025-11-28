FROM python:3.10-slim

LABEL maintainer="Garak Security <support@garak.ai>"
LABEL description="Garak AI Security Scanner for CI/CD pipelines"

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    jq \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    garak-sdk>=0.1.0 \
    requests>=2.31.0

# Copy entrypoint script
COPY entrypoint.py /app/entrypoint.py
RUN chmod +x /app/entrypoint.py

ENTRYPOINT ["python", "/app/entrypoint.py"]
