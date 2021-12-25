import configparser
import json
import pathlib

import boto3
import telebot

DEFAULT = 'default'

path = pathlib.Path(__file__).parent
p = str(path)

cfg = configparser.ConfigParser()
cfg.read('{}/token'.format(p))

token = cfg[DEFAULT]['token']
chat_id = cfg[DEFAULT]['chat_id']

cfg.read('{}/credentials'.format(p))
key_id = cfg[DEFAULT]['aws_access_key_id']
secret_key = cfg[DEFAULT]['aws_secret_access_key']

cfg.read('{}/keys'.format(p))
folder_id = cfg[DEFAULT]['folderId']
api_key = cfg[DEFAULT]['key']
queue_name = cfg[DEFAULT]['queue_name']

cfg.read('{}/config'.format(p))
region = cfg[DEFAULT]['region']

s3 = boto3.client(
    service_name='sqs',
    endpoint_url='https://message-queue.api.cloud.yandex.net',
    aws_access_key_id=key_id,
    aws_secret_access_key=secret_key,
    region_name=region
)
sqs_url = 'https://message-queue.api.cloud.yandex.net'
q_url = 'https://message-queue.api.cloud.yandex.net/b1gs4a51unfsngpt0hke/dj6000000003pfmr06dt/test'

bot = telebot.TeleBot(token)


def handler(event, context):

    print(event)
    json_object = json.loads(json.dumps(event))
    image_path = json_object['messages'][0]['details']['message']['message_attributes']['string']['string_value']
    image_path = image_path[1:-1].split(', ')
    for i in image_path:
        bot.send_message(chat_id=chat_id, text='Кто это?')
        bot.send_photo(chat_id=chat_id, photo=f'https://storage.yandexcloud.net/d01.itiscl.ru/{i[1:-1]}',
                   caption=f'https://storage.yandexcloud.net/d01.itiscl.ru/{i[1:-1]}')

    return {
        'statusCode': 200,
        'body': 'Ok',
    }

