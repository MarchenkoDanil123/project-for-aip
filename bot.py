import telebot
from typing import List, Union
import cmath
import sympy
import math

bot = telebot.TeleBot("2007989606:AAFtUMvumZFDbUKMigNDrq9y1ZpkcrFUDlY")

state = {}
def round_complex(x):
    """
    Функция окргуляет вещественную и мнимую часть комплексного числа до двух знаков после запятой и убирает скобки вокруг числа
    :param x: комплексное число 
    :return: округленное комплексное число без скобок
    """
    return "{:.2f}{:+.2f}j".format(x.real, x.imag)

@bot.message_handler(commands=["start"])
def start(m: telebot.types.Message) -> telebot.types.Message:
    """
    Функция командует созданием 3 кнопок выбора режима и сообщением от бота
    :param m: 
    :return: 3 кнопки с различными режимами калькулятора и просит выбрать один из них
    """
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    items = (telebot.types.InlineKeyboardButton("Решение квадратных уравнений", callback_data="quad"), \
         telebot.types.InlineKeyboardButton("Решение тригонометрических уравнений", callback_data="trigonometry"), \
            telebot.types.InlineKeyboardButton("Решение интегральных уравнений", callback_data="integral"))
    markup.add(*items)
    return bot.send_message(chat_id=m.chat.id, text="Выбери режим", reply_markup=markup)


@bot.callback_query_handler(func=lambda query: True)
def query_handler(call: telebot.types.CallbackQuery):
    """
    Функция проверяет выбранный пользователем режим и выводит соответствующие ему сообщение
    :param call: запрос полученный от пользователя
    :return: сообщение пользователю
    """
    state[call.from_user.id] = call.data
    if call.data == 'quad':
        return bot.send_message(chat_id=call.message.chat.id, text=f"режим изменен на {call.data}, введите три коэффициента через пробел")
    elif call.data == 'trigonometry':
        return bot.send_message(chat_id=call.message.chat.id, text=f"режим изменен на {call.data}, введите градусы и функцию через запятую")
    else:
        return bot.send_message(chat_id=call.message.chat.id, text=f"режим изменен на {call.data}, \
            введите функцию, которая будет интегрирована, а также нижний и верхний пределы через пробелы")

@bot.message_handler(func=lambda message: True)
def calculator(message: telebot.types.Message):
    """
    Вычисляет решение для заданного уравнения на основе текущего состояния и пользовательского ввода.
    :param message: Объект сообщения, полученный от пользователя.
    :return: Cообщение, отправленное пользователю с решением уравнения.
    """
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
            return bot.send_message(chat_id=message.chat.id, text=f"Нет вещественных корней, но есть комплексные:\n\n \
                Первый корень = {x1}\n Второй корень = {x2}")

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
        text = message.text.split(", ")
        angle_in_degrees = float(text[0])
        trig_function = text[1]

        # def trig_calculator(angle_in_degrees, trig_function):
        #     # Convert the angle to radians
        angle_in_radians = math.radians(angle_in_degrees)
            
        if trig_function == "sin":
            result = math.sin(angle_in_radians)
        elif trig_function == "cos":
            result = math.cos(angle_in_radians)
        elif trig_function == "tan" or trig_function == "tg":
            result = math.tan(angle_in_radians)
        elif trig_function == "cot" or trig_function == "ctg":
            result = 1/(math.tan(angle_in_radians))
        else:
           return bot.send_message(chat_id=message.chat.id, text="Неверный ввод функции")
            
        return bot.send_message(chat_id=message.chat.id, text=f" {format(result, '.1f')}")   
    
    elif current_state == 'integral':
        try:
            text = message.text
            parts = text.split()
            if len(parts) != 3:
                raise ValueError("Неверный ввод. Введите через пробел функцию, нижний и верхний пределы")
            function = parts[0]
            lower_limit = parts[1]
            upper_limit = parts[2]

            x = sympy.Symbol('x')
            function = sympy.sympify(function)
            lower_limit = sympy.sympify(lower_limit)
            upper_limit = sympy.sympify(upper_limit)

            result = sympy.integrate(function, (x, lower_limit, upper_limit))

            bot.send_message(message.chat.id, result)
    
        except ValueError:
            bot.send_message(message.chat.id, "Ошибка ввода. Пожалуйста, введите действительные математическое выражение и пределы")

    else:
        return bot.send_message(chat_id=message.chat.id, text="Неверно")

bot.polling(non_stop=True)
    

