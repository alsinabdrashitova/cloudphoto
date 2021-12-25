import telebot
from bot import bot


def handler(event, _):
    print(event)
    message = telebot.types.Update.de_json(event['body'])
    bot.process_new_updates([message])
    return {
        'statusCode': 200,
        'body': '!',
    }