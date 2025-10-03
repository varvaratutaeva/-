import os
import telebot
from bot_logic import gen_pass


    # Замени 'TOKEN' на токен твоего бота
    # Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot("8434288872:AAHWnVxMMSzZuhRs1TKwbyLFUljx1LI6Odc")

text_messages = {
    'welcome':
        u'Please welcome {name}!\n\n'
        u'This chat is intended for questions about and discussion of the pyTelegramBotAPI.\n'
        u'To enable group members to answer your questions fast and accurately, please make sure to study the '
        u'project\'s documentation (https://github.com/eternnoir/pyTelegramBotAPI/blob/master/README.md) and the '
        u'examples (https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples) first.\n\n'
        u'I hope you enjoy your stay here!',

    'info':
        u'My name is TeleBot,\n'
        u'I am a bot that assists these wonderful bot-creating people of this bot library group chat.\n'
        u'Also, I am still under development. Please improve my functionality by making a pull request! '
        u'Suggestions are also welcome, just drop them in this group chat!',

    'wrong_chat':
        u'Hi there!\nThanks for trying me out. However, this bot can only be used in the pyTelegramAPI group chat.\n'
        u'Join us!\n\n'
        u'https://telegram.me/joinchat/067e22c60035523fda8f6025ee87e30b'
}
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши команду /hello, /bye или /pass для генерации пароля")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет, как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока, удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    password=gen_pass(10)
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")


GROUP_CHAT_ID = int(os.environ["GROUP_CHAT_ID"])
def is_api_group(chat_id):
    return chat_id == GROUP_CHAT_ID

@bot.message_handler(commands=['info', 'help'])
def on_info(message):
    if not is_api_group(message.chat.id):
        bot.reply_to(message, text_messages['wrong_chat'])
        return

    bot.reply_to(message, text_messages['info'])

@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "Still alive and kicking!")
@bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
def on_user_joins(message):
    if not is_api_group(message.chat.id):
        return

    name = message.new_chat_participant.first_name
    if hasattr(message.new_chat_participant, 'last_name') and message.new_chat_participant.last_name is not None:
        name += u" {}".format(message.new_chat_participant.last_name)

    if hasattr(message.new_chat_participant, 'username') and message.new_chat_participant.username is not None:
        name += u" (@{})".format(message.new_chat_participant.username)

    bot.reply_to(message, text_messages['welcome'].format(name=name))
    
bot.polling()
