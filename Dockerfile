FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY *.py .

# 暴露端口（根据实际应用调整）
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]
