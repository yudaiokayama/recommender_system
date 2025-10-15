# Pythonの公式イメージをベースに使用
FROM python:3.12

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 必要なライブラリをインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# Flaskが使用するポートを公開
EXPOSE 5000
