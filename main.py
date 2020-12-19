import os
import time
import requests
import telegram
import logging

logger = logging.getLogger("Bot Logger")


class TelegramBotLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger.setLevel(logging.DEBUG)
    devman_token = os.environ['DEVMAN_TOKEN']
    headers = {
        'Authorization': devman_token
    }
    params = {
        'timestamp': ''
    }
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    bot = telegram.Bot(token=telegram_token)
    logger.addHandler(TelegramBotLogsHandler(bot, chat_id))
    logger.debug('Информирование о курсе запущено')

    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=params, timeout=240)
            response.raise_for_status()
        except ConnectionError as er:
            time.sleep(30)
            logger.exception(er)
            continue
        except requests.exceptions.ReadTimeout as er:
            logger.info(er)
            continue
        response = response.json()
        if response['status'] == 'timeout':
            params['timestamp'] = response['timestamp_to_request']
        elif response['status'] == 'found':
            new_attempt = response['new_attempts'][0]
            lesson = new_attempt['lesson_title']
            if new_attempt['is_negative']:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson}"\n\nК сожалению, в '
                                                       f'работе нашлись ошибки.')
            else:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson}"\n\nПреподавателю все'
                                                       f' понравилось, можо приступать к следующему уроку!')
            params['timestamp'] = response['last_attempt_timestamp']


if __name__ == '__main__':
    main()
