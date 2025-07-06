# 使用官方 Python 映像檔作為基礎
FROM python:3.11-alpine

# 設定工作目錄
WORKDIR /app

# 將 requirements.txt 複製到容器中並安裝依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 將應用程式程式碼複製到容器中
COPY . .

# 定義啟動應用程式的命令
CMD ["python", "app.py"]