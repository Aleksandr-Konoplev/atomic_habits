import requests

from config.settings import TG_BOT_TOKEN


def send_message_to_tg(chat_id: str, message: str):

    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=data)


if __name__ == '__main__':
    chat = '475506333'
    mess = 'qwe'

    send_message_to_tg(chat, mess)
