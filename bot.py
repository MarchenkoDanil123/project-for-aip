import telebot
from typing import List, Union


bot = telebot.TeleBot("2007989606:AAFtUMvumZFDbUKMigNDrq9y1ZpkcrFUDlY")

state = {}

@bot.message_handler(commands=["start"])
def start(m: telebot.types.Message) -> telebot.types.Message:
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    items = (telebot.types.InlineKeyboardButton("Решение квадратных уравнений", callback_data="quad"), \
         telebot.types.InlineKeyboardButton("Решение тригонометрических уравнений", callback_data="trigonometry"), \
            telebot.types.InlineKeyboardButton("Решение интегральных уравнений", callback_data="integral"))
    markup.add(*items)
    return bot.send_message(chat_id=m.chat.id, text="Выбери режим", reply_markup=markup)


@bot.callback_query_handler(func=lambda query: True)
def query_handler(call: telebot.types.CallbackQuery):
    state[call.from_user.id] = call.data
    return bot.send_message(chat_id=call.message.chat.id, text=f"режим изменен на {call.data}, введи коэффициенты через пробел")

@bot.message_handler(func=lambda message: True)
def quad(message: telebot.types.Message):
    current_state = state.get(message.from_user.id, None)
    if current_state == 'quad':
        text = message.text
        kf = text.split()
        if len(kf) != 3:
            return bot.send_message(chat_id=message.chat.id, text="введи 3 числа")
        try:
            kf = list(map(float, kf))
        except Exception:
            return bot.send_message(chat_id=message.chat.id, text="введи числа")

        a, b, c = kf
        D = (b ** 2) - (4 * a * c)
        if D < 0:
            return bot.send_message(chat_id=message.chat.id, text="нет корней")
        if D == 0:
            x = -b / 2 * a
            return bot.send_message(chat_id=message.chat.id, text=f"один корень: {int(x)}")

        x1: float = (-b - D ** 0.5) / (2 * a)
        x2: float = (-b + D ** 0.5) / (2 * a)

        if int(x1).endswith('.0'):
            x1 = int(x1)
        if int(x2).endswith('.0'):
            x2 = int(x2)    
        return bot.send_message(chat_id=message.chat.id, text=f'*Корни:*\n\nПервый корень: *{str(x1)}*\nВторой корень: *{str(x2)}*', parse_mode='Markdown')
    elif current_state == 'trigonometry':
        text = message.text
        text = text.replace(" ", "")
        mass = list(text)
        result: List[Union[str, int, float]] = []
        k = ""
        for i in mass:
            if i.isdigit():
                k += i
            else:
                result.append (int(k))
        return bot.send_message(chat_id=message.chat.id, text=f" {result}")       

    else:
        return bot.send_message(chat_id=message.chat.id, text="Неверно")
bot.polling(non_stop=True)

