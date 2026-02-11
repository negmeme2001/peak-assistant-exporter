FROM python:3.10-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv pip install --system -e .

COPY src/ src/

EXPOSE 8000

CMD ["python", "src/main.py"]
