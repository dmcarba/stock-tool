# -------- Builder --------
FROM python:3.11-alpine AS builder

RUN apk add --no-cache build-base gcc musl-dev libffi-dev

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry==1.4 \
 && poetry export -f requirements.txt --without-hashes -o requirements.txt \
 && pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# -------- Runtime --------
FROM python:3.11-alpine

WORKDIR /app

# Install runtime deps only (no compilers)
RUN apk add --no-cache libffi

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY stock_tool/ ./stock_tool/

ENV API_PORT=8001
ENV MCP_PORT=3001

EXPOSE 3001
EXPOSE 8001

CMD ["python", "-m", "stock_tool.stock_tool"]