FROM python:3.12-slim

WORKDIR /app

# Copy everything from root into the container
COPY . /app

# Optional: ensure PYTHONPATH includes /app for clean absolute imports
# ENV PYTHONPATH=/app

RUN pip install fastapi uvicorn langgraph langchain-core typing-extensions httpx python-dotenv langchain-ollama ipython

EXPOSE 8000

CMD ["uvicorn", "src.graph.main:app", "--host", "0.0.0.0", "--port", "8000"]
