FROM python:3.9-alpine
WORKDIR /devman_bot
COPY requirements.txt .
RUN apk update && pip install -r requirements.txt
COPY . .
CMD ["python", "devman_api.py"]