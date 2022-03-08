# devman_bot
This bot send requests to DevMan API and then sends notification when one of the work will check

How to run:
1. git clone https://github.com/Hyper-glitch/devman_bot.git
2. create your own .env file with DEVMAN_TOKEN (token from devman API), TG_TOKEN(access token from BotFather in telegram), CHAT_ID(id from userinfobot) and USERNAME(your name)
3. building docker image: _**docker build -t image_name .**_
4. run container: **_docker run --env-file .env image_name_**
