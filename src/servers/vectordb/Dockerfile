FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn pydantic langchain-core langchain-nomic langchain-community langchain bs4 tiktoken ipython scikit-learn nomic[local]

EXPOSE 8000

CMD ["uvicorn", "src.servers.vectordb.main:app", "--host", "0.0.0.0", "--port", "8000"]
