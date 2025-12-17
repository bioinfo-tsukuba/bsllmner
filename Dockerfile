FROM python:3.10-alpine

# 依存ライブラリをインストール
RUN pip3 install --no-cache-dir ollama pyyaml openai

# アプリ配置
WORKDIR /app/bsllmner
COPY . /app/bsllmner

ENTRYPOINT ["python3", "-m", "bsllmner"]
CMD ["-h"]
