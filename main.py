import os
import time
import requests
import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    headers = {
        'Authorization': devman_token
    }
    params = {
        'timestamp': ''
    }
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(token=telegram_token)

    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=params)
            response.raise_for_status()
        except (requests.exceptions.ReadTimeout, ConnectionError):
            time.sleep(3)
            continue
        response = response.json()
        new_attempts = response['new_attempts'][0]
        if response['status'] == 'timeout':
            params['timestamp'] = response['timestamp_to_request']
        elif response['status'] == 'found':
            lesson = new_attempts['lesson_title']
            if new_attempts['is_negative']:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson}"\n\nК сожалению, в '
                                                       f'работе нашлись ошибки.')
            else:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson}"\n\nПреподавателю все'
                                                       f' понравилось, можо приступать к следующему уроку!')
            params['timestamp'] = response['last_attempt_timestamp']


if __name__ == '__main__':
    main()
