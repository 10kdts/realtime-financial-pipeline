FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY data/sample/events.jsonl ./data/sample/events.jsonl
CMD ["python", "-m", "realtime_finance.processor", "--input", "data/sample/events.jsonl", "--db", "data/pipeline.db", "--replay"]

