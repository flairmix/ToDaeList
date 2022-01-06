from replit import db
import os
import telebot
from datetime import date

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['help'])
def help(message):
    str_output = "Привет, милая! \n\
    \n\
    Лист комманд: \n\
    /list - Посмотреть список;\n\
    /new - Добавить новую строку;\n\
        (нажать на /new -> ввести новую строку)\n\
    \n\
    /check - Отметить \"галочкой\";\n\
    /uncheck - Отметить \"крестиком\";\n\
    /del_last - Удалить последнюю строку;"

    bot.send_message(message.chat.id, str_output)


# @bot.message_handler(commands=['create_todolist'])
# def create_todolist(message):
#     db["todolist"] = {
#         '1':  u'\U00002716' + "Посмотреть ведьмака",
#         '2':  u'\U00002716' + "Приготовить борщ",
#         '3':  u'\U00002716' + "Посмотреть Himym на английском",
#         '4':  u'\U00002716' + "Обсудить NFT",
#         '5':  u'\U00002716' + "Гарри Поттер",
#         }
#     bot.send_message(message.chat.id, "done")


@bot.message_handler(commands=['list'])
def list(message):

    tx_output = ""
    if db["todolist"] and len(db["todolist"]) > 0:
        for i in db["todolist"]:
            text = str(i) + " - " + db["todolist"].get(str(i)) + "\n"
            tx_output += text
        bot.send_message(message.chat.id, tx_output)
    else:
        bot.send_message(message.chat.id, "list_empty")


@bot.message_handler(commands=["new"])
def new_list_item(message):
    msg = bot.reply_to(message, "Input new list's item")
    bot.register_next_step_handler(msg, write_new_list_item)


def write_new_list_item(message):
    try:
        chat_id = message.chat.id
        new_list_item = u'\U00002716'+ message.text
        add_item(new_list_item)
        index = str(len(db["todolist"]) )
        bot.send_message(message.chat.id, (f"Item #{index} has been added " + " - " + new_list_item))
    except Exception as e:
        bot.reply_to(message, e)


def add_item(item_text):
    index = str(len(db["todolist"]) + 1)
    db["todolist"][index] = item_text


@bot.message_handler(commands=["del_last"])
def del_last(message):
    if db["todolist"] and len(db["todolist"]) > 0:
        del db["todolist"][str(len(db["todolist"]))]
        bot.send_message(message.chat.id, "last item has been deleted")
    else:
        bot.send_message(message.chat.id, "list_empty")


@bot.message_handler(commands=["check"])
def check(message):
    msg = bot.reply_to(message, "Input number of item in list for \"check\"")
    bot.register_next_step_handler(msg, check_list_item)


def check_list_item(message):
    try:
        chat_id = message.chat.id
        list_item = message.text
        check_item(list_item)
        bot.send_message(message.chat.id, (f"Item #{list_item} has been checked" ))
    except Exception as e:
        bot.reply_to(message, e)

def check_item(item):
    if str(item) in db["todolist"].keys():
        text = u'\U00002714' + db["todolist"][str(item)][1:] + " [" + date.today().strftime('%Y/%m/%d') + "]"
        db["todolist"][str(item)] = text


@bot.message_handler(commands=["uncheck"])
def uncheck(message):
    msg = bot.reply_to(message, """\
Input number list's item for "uncheck"
""")
    bot.register_next_step_handler(msg, uncheck_list_item)


def uncheck_list_item(message):
    try:
        chat_id = message.chat.id
        list_item = message.text
        uncheck_item(list_item)
        bot.send_message(message.chat.id, (f" Item {list_item} has been unchecked"))
    except Exception as e:
        bot.reply_to(message, e)


def uncheck_item(item):
    if str(item) in db["todolist"].keys():
        if db["todolist"][str(item)].find(u'\U00002714') != -1:
            text = u'\U00002716' + db["todolist"][str(item)][1:-12]
            db["todolist"][str(item)] = text




bot.polling()