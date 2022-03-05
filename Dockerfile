FROM python:3.9-alpine
WORKDIR /devman_bot
ADD requirements.txt .
python -m pip install --upgrade pip && \
pip install -r requirements.txt
ADD . .