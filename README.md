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

## To deploy on server:
The fastest way to deploy on server it's getting Heroku account and connect it with your GitHub Rep.
You should make your fork of repository, all files including `requirements.txt` and `Pocfile` should be inside repo.
Follow the prompts to deploy from GitHub!

***DON'T PUT YOUR SENSITIVE INFORAMTION IN YOUR CODE!!!***

Heroku has it's own settings inside the service to provide safe method of getting your environment variables.
Put your variables from `.env` file to [special fields](https://prnt.sc/vnv8w9)in Heroku app settings.
Use Heroku CommandLine App to traceback Errors. If everything ok, you'll see "https://prnt.sc/vnvb5g.

