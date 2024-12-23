FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN python -m grpc_tools.protoc -I./protobufs --python_out=. --grpc_python_out=. ./protobufs/dictionary.proto

EXPOSE 50051 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
