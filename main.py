import os
import time
import requests
import telegram
import logging


class TelegramBotLogsHandler(logging.Handler, telegram.Bot):
    def emit(self, record):
        log_entry = self.format(record)
        self.send_message(chat_id=os.environ['TELEGRAM_CHAT_ID'], text=f'{log_entry}')


class MyBot(telegram.Bot, logging):
    def __init__(self, token):
        super().__init__(token, base_url=None, request=None, private_key=None, private_key_password=None, defaults=None)
        self.logging("Бот запущен")


def main():
    logger = logging.getLogger("Bot Logger")
    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramBotLogsHandler())

    devman_token = os.environ['DEVMAN_TOKEN']
    headers = {
        'Authorization': devman_token
    }
    params = {
        'timestamp': ''
    }
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    bot = MyBot(token=telegram_token)

    try:
        0 / 0
    except Exception:
        logger.exception()

    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=params, timeout=91)
            response.raise_for_status()
        except ConnectionError:
            time.sleep(30)
            continue
        except requests.exceptions.ReadTimeout:
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
