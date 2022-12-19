import telebot
from typing import List, Union
import cmath

bot = telebot.TeleBot("2007989606:AAFtUMvumZFDbUKMigNDrq9y1ZpkcrFUDlY")

state = {}
def round_complex(x):
    return "{:.2f}{:+.2f}j".format(x.real, x.imag)

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
    if call.data == 'quad':
        return bot.send_message(chat_id=call.message.chat.id, text=f"режим изменен на {call.data}, введи коэффициенты через пробел")
    elif call.data == 'trigonometry':
        return bot.send_message(chat_id=call.message.chat.id, text=f"режим изменен на {call.data}")
    else:
        return bot.send_message(chat_id=call.message.chat.id, text=f"режим изменен на {call.data}")
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
        if kf[0] == 0 or kf[1] == 0 or kf[2] == 0:
            return bot.send_message(chat_id=message.chat.id, text="коэффицент не должен быть равен нулю")

        a, b, c = kf
        D = int(b ** 2) - (4 * a * c)

    
        if D < 0:
            x1 = round_complex((-b + cmath.sqrt(D)) / (2*a))
            x2 = round_complex((-b - cmath.sqrt(D)) / (2*a))    
            return bot.send_message(chat_id=message.chat.id, text=f"Нет вещественных корней, но есть комплексные:\n\n Первый корень = {x1}\n Второй корень = {x2}")

        if D == 0:
            x = -b / 2 * a
            return bot.send_message(chat_id=message.chat.id, text=f"один корень: {int(x)}")

        x1: float = (-b - D ** 0.5) / (2 * a)
        x2: float = (-b + D ** 0.5) / (2 * a)

        if str(x1).endswith('.0'):
            x1 = int(x1)
        if str(x2).endswith('.0'):
            x2 = int(x2)    
        return bot.send_message(chat_id=message.chat.id, text=f'Дискриминант = *{D}*\n\n *Корни:*\nПервый корень = {format(x1,".3f")}\nВторой корень = {format(x2, ".3f")}', parse_mode='Markdown')
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
