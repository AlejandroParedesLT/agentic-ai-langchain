FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn pydantic python-dotenv langchain langchain-core langchain-ollama ipython

EXPOSE 8000

CMD ["uvicorn", "src.servers.documentGrader.main:app", "--host", "0.0.0.0", "--port", "8000"]
