# devman_bot
---

## Basic information

***Devman bot*** sends requests to DevMan API and then sends notification to telegram bot, when one of the work is checked.

<ins>*Notification* includes:</ins>  
- Username;
- Lesson title;
- Lesson URL;
- Message with success or failure status.

## Running

Create **.env** file and set the <ins>following environmental variables</ins>:  

| Environmental      | Description                                           |
|--------------------|-------------------------------------------------------|
| `DEVMAN_TOKEN`     | personal student token from *dvmn.org* to use its API |       
| `TG_TOKEN`         | telegram bot token from @BotFather                    |      
| `CHAT_ID`          | your chat id from @userinfobot                        |
| `USERNAME`         | your name                                             |

Run with a docker container with the following commands:
```bash
docker build -t devman_bot . && docker run --env-file .env devman_bot
```
Run without a container

1. clone the repository:
```bash
git clone https://github.com/Hyper-glitch/devman_bot.git
```
2. Create **.env** file and set the <ins>environmental variables</ins> as described above.
3. Create venv
```bash
python3 -m venv venv
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Run python script
```bash
python3 main.py
```
