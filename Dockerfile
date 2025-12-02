FROM python:3.10-alpine

# 依存ライブラリをインストール
RUN pip3 install --no-cache-dir ollama pyyaml openai

# アプリ配置
WORKDIR /app/bsllmner
COPY . /app/bsllmner

# パッケージとしてインストール（モジュール参照を安定化）
RUN pip3 install --no-cache-dir .

ENTRYPOINT ["python3", "-m", "bsllmner"]
CMD ["-h"]
