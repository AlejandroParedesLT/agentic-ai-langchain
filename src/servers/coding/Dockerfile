FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn pydantic langchain-core langchain-community rizaio

EXPOSE 8000

CMD ["uvicorn", "src.servers.coding.main:app", "--host", "0.0.0.0", "--port", "8000"]
