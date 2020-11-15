# TELEGRAM NOTIFICATION
Designed to help devman students getting response and code review faster.
It takes information through devman API and send notification to your telegram.

## How to install:
 - Python3 should be already installed on PC.
 - Python dependencies file is `requirements.txt`.
 - Execute in command line `pip3 install -r requirements.txt` to install dependencies
## To run program:
 1. You should get bot API and paste it to `.env`. Find `@botfather` in your telegram and write `/newbot` 
 and follow the instructions. 
  `TELEGRAM_TOKEN='your_token'`
 2. Get your telegram chat id. (One way is to send `/sart` to `@userinfobot`)
  Put given id into `TELEGRAM_CHAT_ID` variable.
  `TELEGRAM_CHAT_ID='your_chat_id'`
 3. Put your [devman token](https://dvmn.org/api/docs/) to `.env`.  
`DEVMAN_TOKEN='your_token'`
4. Execute python `main.py` from your command line. Program getting information in the through API 
while `main.py` is running.