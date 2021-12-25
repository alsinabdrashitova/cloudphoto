import configparser
import pathlib

import telebot
import boto3

DEFAULT = 'default'

path = pathlib.Path(__file__).parent
p = str(path)

cfg = configparser.ConfigParser()
cfg.read('{}/key'.format(p))

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

bot = telebot.TeleBot(token)

s3 = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=key_id,
    aws_secret_access_key=secret_key,
    region_name=region
)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, f'Привет')


@bot.message_handler(commands=['name'])
def name_command(message):
    if message.reply_to_message is not None:
        caption = message.json['reply_to_message']['caption']
        name = message.json['text'][6:]
        link_arr = caption.split("/")
        original_photo = f'{link_arr[0]}' \
                         f'/{link_arr[1]}/' \
                         f'{link_arr[2]}/' \
                         f'{link_arr[3]}/' \
                         f'{link_arr[4]}/' \
                         f'{link_arr[5].replace("_jpg_r", ".jpg_r")}'

        print(original_photo)
        if name:
            print(f'{name}')
            put(name, original_photo)
            bot.send_message(message.chat.id, 'Я запомнил')
        else:
            bot.send_message(message.chat.id, 'Введите имя')
    else:
        bot.send_message(message.chat.id, 'А где фотография?))0)')


def put(name, orig_photo):
    s3.put_object(Body=f'{name}@{orig_photo}', Bucket='d01.itiscl.ru',
                  Key=f'{name}@{orig_photo.replace("/", "#")}.txt')

@bot.message_handler(commands=['id'])
def chat_id_command(message):
    bot.send_message(chat_id=message.chat.id, text=f'{message.chat.id}')


@bot.message_handler(commands=['find'])
def find_command(message):
    print(message)
    name = message.json['text'][6:]
    print(f'{name}')
    resp = s3.list_objects_v2(Bucket='d01.itiscl.ru')

    obj_arr = []
    for obj in resp['Contents']:
        new_obg = obj['Key'].split('@')
        if str(new_obg[0].strip()) == str(name.strip()):
            obj_arr.append(new_obg[1])

    if len(obj_arr) > 0:
        for o in obj_arr:
            o = o.replace('#', '/')
            o = o.replace('.txt', '')
            print(o)
            bot.send_message(chat_id=message.chat.id, text='Вот')
            bot.send_message(chat_id=message.chat.id, text=f'{o}')
            bot.send_photo(chat_id=message.chat.id, photo=f'{o}')
    else:
        bot.send_message(chat_id=message.chat.id, text='Я не знаю кто это')
