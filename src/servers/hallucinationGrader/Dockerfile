FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn pydantic langchain-core python-dotenv langchain-ollama langgraph ipython langchain

EXPOSE 8000

CMD ["uvicorn", "src.servers.hallucinationGrader.main:app", "--host", "0.0.0.0", "--port", "8000"]
