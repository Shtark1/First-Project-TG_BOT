import telebot
from telebot import types
import random
from random import choices, sample
import string
from random import choice



token = "5063547879:AAGyxpCAALWjyuOeEspuCLvyhKufwxIKxi0"

bot = telebot.TeleBot(token)

info = """Бот создан @svirin2000"""

password = []  # Хранит все пароли которые создовались рандомно

savepassword = []  # Хронит сохранённные пароли

quantity = [] # количество символов


@bot.message_handler(commands=["help", "start"])  # Начало
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("⚒Создать пароль⚒")
    item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
    item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
    item4 = types.KeyboardButton("📚Информация📚")

    markup.add(item1, item2) # создание наших кнопок
    markup.add(item3)
    markup.add(item4)
    bot.send_message(message.chat.id, "Привет, {0.first_name}🥸\nЭтот бот поможет тебе с созданием и сохранением твоих паролей!!".format(message.from_user), reply_markup = markup)


@bot.message_handler(commands=["subscribe"])  # Код для подписи пароля
def subscribe(message):
    bot.send_message(message.chat.id, "Подпиши пароль✍️")
    bot.register_next_step_handler(message, subscribe2)
def subscribe2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("⚒Создать пароль⚒")
    item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
    item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
    item4 = types.KeyboardButton("📚Информация📚")

    markup.add(item1, item2)
    markup.add(item3)
    markup.add(item4)

    name = message.text
    namepassword = name + ":\n" + password[-1]  # Добавление имени
    savepassword.append(namepassword)

    bot.send_message(message.chat.id, "Ваш пароль подписан\n📝".format(message.from_user), reply_markup = markup)


@bot.message_handler(commands=["save"])    # Сохранение пароя без подписи
def save(message):
    savepassword.append(password[-1])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("⚒Создать пароль⚒")
    item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
    item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
    item4 = types.KeyboardButton("📚Информация📚")

    markup.add(item1, item2)
    markup.add(item3)
    markup.add(item4)
    bot.send_message(message.chat.id, "Ваш пароль сохранён\n✅".format(message.from_user), reply_markup = markup)


@bot.message_handler(commands=["creat_password"])    # Создание рандомного пароля
def creat(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("8")
    item2 = types.KeyboardButton("12")
    item3 = types.KeyboardButton("16")
    item4 = types.KeyboardButton("20")
    item5 = types.KeyboardButton("24")
    item6 = types.KeyboardButton("28")
    item7 = types.KeyboardButton("⬅️Меню")
    markup.add(item1, item2, item3)
    markup.add(item4, item5, item6)
    markup.add(item7)
    bot.send_message(message.chat.id, "Напиши нужное количество символов в пароле\nДо 💯 символов:".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, creat2)
def creat2(message):
    quanti = message.text
    if len(quanti) == 6:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚒Создать пароль⚒")
        item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
        item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
        item4 = types.KeyboardButton("📚Информация📚")

        markup.add(item1, item2)  # создание наших кнопок
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id,"Выбери любую функцию🤖".format(message.from_user), reply_markup=markup)
    else:
        try:
            if 1 <= int(quanti) <= 100:
                quantity.append(int(quanti))
                texts = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=quantity[-1]))  # Усовершенствование кода Цифры Буквы и строчные и заглавные спецсимволы
                password.append(texts)
                keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
                key_yes = types.InlineKeyboardButton(text='Оставить', callback_data='yes') # кнопка «Да»
                keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
                key_no = types.InlineKeyboardButton(text='Поменять', callback_data='no');
                keyboard.add(key_no)
                question = texts + "\nСохранить этот пароль или поменять?"
                bot.send_message(message.chat.id, text=question, reply_markup=keyboard)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Повторить")
                markup.add(item1)
                bot.send_message(message.chat.id, "❌число введено не коректно❌\nПовтори ввод нужного количества символов".format(message.from_user), reply_markup=markup)
                bot.register_next_step_handler(message, creat)
        except ValueError:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Повторить")
            markup.add(item1)
            bot.send_message(message.chat.id, "❌число введено не коректно❌\nПовтори ввод нужного количества символов".format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, creat)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("/subscribe")
        item2 = types.KeyboardButton("/save")
        item3 = types.KeyboardButton("⬅️Меню")
        markup.add(item1, item2)
        markup.add(item3)
        bot.send_message(call.message.chat.id, 'Пароль: ' + password[-1] + "\n/subscribe чтобы подписать пароль\nили\n/save чтобы сохранить так".format(call.from_user), reply_markup = markup)
    elif call.data == "no":
        texts = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=quantity[-1]))  # Усовершенствование кода Цифры Буквы и строчные и заглавные спецсимволы
        password.append(texts)
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Оставить', callback_data='yes') # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Поменять', callback_data='no');
        keyboard.add(key_no)
        question = texts + "\nСохранить этот пароль или поменять?"
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)


@bot.message_handler(commands=["add_password"])   # Добавление своего пароля
def add(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Запиши пароль✍️")
    item2 = types.KeyboardButton("⬅️Меню")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, "Запиши свой пароль, не более 💯 символов".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, add2)
def add2(message):
    passw = message.text
    if passw == "⬅️Меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚒Создать пароль⚒")
        item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
        item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
        item4 = types.KeyboardButton("📚Информация📚")
        markup.add(item1, item2)  # создание наших кнопок
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, "Выбери любую функцию🤖".format(message.from_user), reply_markup=markup)
    else:
        if len(passw) < 101:
            password.append(passw)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("/subscribe")
            item2 = types.KeyboardButton("/save")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Пароль: ' + password[-1] + "\n/subscribe чтобы подписать пароль\nили\n/save чтобы сохранить".format(message.from_user), reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Повторить")
            item2 = types.KeyboardButton("⬅️Меню")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Слишком длинный пароль, хотите повторить ввод или выйти в меню?".format(message.from_user), reply_markup = markup)
            bot.register_next_step_handler(message, add3)
def add3(message):
    len_message = message.text
    if len(len_message) == 9:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Повторить")
        markup.add(item1)
        bot.register_next_step_handler(message, add)
        bot.send_message(message.chat.id, "Хорошо\nТогда жми кнопку повторить ещё раз и записывай свой пароль🥸".format(message.from_user), reply_markup = markup)


@bot.message_handler(commands=["delete"])    # Удаление пароля из сохр
def delete(message):
    bot.send_message(message.chat.id, "Ваши пароли:")
    if len(savepassword) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚒Создать пароль⚒")
        item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
        item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
        item4 = types.KeyboardButton("📚Информация📚")

        markup.add(item1, item2)  # создание наших кнопок
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, "Пока список пуст, удалять нечего😟".format(message.from_user), reply_markup = markup)

    elif len(savepassword) > 0:
        i = 0
        a = 1
        while i < len(savepassword):
            bot.send_message(message.chat.id, str(a) + ". " + savepassword[i])
            i += 1
            a +=1
        bot.send_message(message.chat.id, "Напиши цифру того пароля который хочешь удалить")
        bot.register_next_step_handler(message, delete2)
def delete2(message):
    try:
        number = int(message.text) - 1
        if number < len(savepassword):
            del savepassword[number]
            bot.send_message(message.chat.id, "Пароль успешно удалён из списка❎\nОставшиеся пароли:")
            if len(savepassword) == 0:
                bot.send_message(message.chat.id, "Список пуст❌")
            elif len(savepassword) > 0:
                i = 0
                while i < len(savepassword):
                    bot.send_message(message.chat.id, savepassword[i])
                    i += 1
        else:
            bot.send_message(message.chat.id, "Под этим номером нет пароля⚠️")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚒Создать пароль⚒")
        item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
        item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
        item4 = types.KeyboardButton("📚Информация📚")

        markup.add(item1, item2)  # создание наших кнопок
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, "Выбери любую функцию🤖".format(message.from_user), reply_markup=markup)

    except ValueError:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚒Создать пароль⚒")
        item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
        item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
        item4 = types.KeyboardButton("📚Информация📚")

        markup.add(item1, item2)  # создание наших кнопок
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, "Введено не коректное число⚠️".format(message.from_user),reply_markup=markup)





@bot.message_handler(content_types=["text"])  # все кнопки и перемещение по меню после start
def bot_message(message):
    if message.chat.type == "private":
        if message.text == "⚒Создать пароль⚒":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("⬅️Меню")
            item1 = types.KeyboardButton("/creat_password")
            item2 = types.KeyboardButton("/add_password")
            markup.add(item1, item2)
            markup.add(back)
            bot.send_message(message.chat.id, "Выбери команду:\n/creat_password  для создания рандомного пароля\nили\n/add_password для добавление своего пароля".format(message.from_user), reply_markup=markup)


        elif message.text == "⬅️Меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("⚒Создать пароль⚒")
            item2 = types.KeyboardButton("Посмотреть все \n🔎пароли🔍")
            item3 = types.KeyboardButton("⛔️Удалить пароль⛔️")
            item4 = types.KeyboardButton("📚Информация📚")
            markup.add(item1, item2)  # создание наших кнопок
            markup.add(item3)
            markup.add(item4)
            bot.send_message(message.chat.id, "Выбери любую функцию🤖".format(message.from_user), reply_markup=markup)


        elif message.text == "📚Информация📚":
            bot.send_message(message.chat.id, info)


        elif message.text == "⛔️Удалить пароль⛔️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("/delete")
            back = types.KeyboardButton("⬅️Меню")
            markup.add(item1)
            markup.add(back)
            bot.send_message(message.chat.id, "/delete команда для удаления сохранённого пароля".format(message.from_user), reply_markup=markup)


        elif message.text == "Посмотреть все \n🔎пароли🔍":
            bot.send_message(message.chat.id, "Ваши пароли:")
            if len(savepassword) == 0:
                bot.send_message(message.chat.id, "  Пока список пуст😟")
            elif len(savepassword) > 0:
                i = 0
                while i < len(savepassword):
                    bot.send_message(message.chat.id, savepassword[i])
                    i+=1

bot.polling(none_stop=True)