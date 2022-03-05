# devman_bot
This bot send requests to DevMan API and then sends notification when one of my work will check

How to run:
1. git clone https://github.com/Hyper-glitch/devman_bot.git
2. create your own .env file with DEVMAN_TOKEN, TG_TOKEN, CHAT_ID
3. building docker image: _**docker build -t image_name .**_
4. run container: **_docker run --env-file .env --name image_name_**