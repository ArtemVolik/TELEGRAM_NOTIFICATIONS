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
    chat_id = os.getenv('CHAT_ID')
    bot = telegram.Bot(token=telegram_token)

    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=params)
            response.raise_for_status()
        except (requests.exceptions.ReadTimeout, ConnectionError):
            time.sleep(3)
            continue
        response = response.json()
        if response['status'] == 'timeout':
            params['timestamp'] = response['timestamp_to_request']
        elif response['status'] == 'found':
            lesson = response['new_attempts'][0]['lesson_title']
            if response['new_attempts'][0]['is_negative']:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson}"\n\nК сожалению, в '
                                                       f'работе нашлись ошибки.')
            else:
                bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson}"\n\nПреподавателю все'
                                                       f' понравилось, можо приступать к следующему уроку!')
            params['timestamp'] = response['last_attempt_timestamp']


if __name__ == '__main__':
    main()
