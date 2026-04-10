FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# 复制应用代码
COPY . .

# 创建存储目录
RUN mkdir -p /app/storage/uploads /app/storage/parsed /app/storage/reports /app/logs

# 暴露端口
EXPOSE 8000

# 运行
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
