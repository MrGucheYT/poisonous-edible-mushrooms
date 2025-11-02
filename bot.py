import telebot
from config import token
from logic import get_class

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Telegram бот. Я научу тебя заботиться об окружающей среде!")

@bot.message_handler(commands=['sortirovka'])
def send_sortirovka(message):
    bot.reply_to(message, "Мусорный бак зелёного цвета - для стекла. А в красный бак нужно класть металл. В синий контейнер - бумагу, а в жёлтый - пластик")

@bot.message_handler(commands=['novosti'])
def send_sortirovka(message):
    bot.reply_to(message, "Вот ссылка на самые новые новость в мире экологии: https://ecosphere.press/news/?ysclid=mbxe4llnq9420301768")

@bot.message_handler(commands=['help'])  
def handle_help(message):  
    help_text = (  
        "/start - Начать работу с ботом\n"  
        "/help - Получить список команд\n"  
        "/sortirovka - Рассказывает о сортировке мусора\n"
        "/novosti - Даёт ссылку на все свежие новости об экологии\n"
    )    
    bot.send_message(message.chat.id, help_text)  

@bot.message_handler(content_types=['photo'])
def send_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    result,conf = get_class(model_path="./keras_model.h5", labels_path="labels.txt",image_path=file_name)

    if result == "edible\n":
        bot.send_message(message.chat.id,f'Данный гриб съедобный!')

    elif result == "poisonous\n":
        bot.send_message(message.chat.id,f'Данный гриб ядовитый!!')

bot.polling()