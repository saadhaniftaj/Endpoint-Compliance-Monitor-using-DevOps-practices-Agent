FROM python:3.11-slim

# Create non-root user
RUN useradd -m agentuser

USER agentuser
WORKDIR /app

COPY --chown=agentuser:agentuser main.py .

RUN pip install --no-cache-dir requests

ENTRYPOINT ["python", "main.py"]