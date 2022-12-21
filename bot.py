import telebot
from typing import List, Union
import cmath
import sympy
import math
import numpy as np
import matplotlib.pyplot as plt


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
    Создает пять кнопок, которые позволяют пользователю выбрать режим для калькулятора, и отправляет сообщение с просьбой выбрать один из них.а
    :param m: данные пользователя
    :return: 5 кнопок с различными режимами калькулятора и просит выбрать один из режимов
    """
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    items = (telebot.types.InlineKeyboardButton("Решение квадратных уравнений", callback_data="quad"),
        telebot.types.InlineKeyboardButton("Решение кубических уравнений", callback_data="cubic"),
            telebot.types.InlineKeyboardButton("Решение уравнений четвёртой степени", callback_data="quartic"),
                telebot.types.InlineKeyboardButton("Решение тригонометрических уравнений", callback_data="trigonometry"),
                    telebot.types.InlineKeyboardButton("Решение интегральных уравнений", callback_data="integral")
            )         
    markup.add(*items)
    bot.send_message(chat_id=m.chat.id, text="Выбери режим", reply_markup=markup)
    return 1


@bot.callback_query_handler(func=lambda query: True)
def query_handler(call: telebot.types.CallbackQuery):
    """
    Функция проверяет выбранный пользователем режим и выводит соответствующие ему сообщение
    :param call: запрос полученный от пользователя
    :return: сообщение пользователю
    """
    state[call.from_user.id] = call.data
    if call.data == 'quad':
        bot.send_message(chat_id=call.message.chat.id,
                            text=f"режим изменен на {call.data}, введите коэффициенты через пробел")
        return 1
    elif call.data == 'cubic':
        bot.send_message(chat_id=call.message.chat.id,
                            text=f"режим изменен на {call.data}, введите коэффициенты через пробел")
    elif call.data == 'quartic':
        bot.send_message(chat_id=call.message.chat.id,
                            text=f"режим изменен на {call.data}, введите коэффициенты через пробел")                       
        return 1
    elif call.data == 'trigonometry':
        bot.send_message(chat_id=call.message.chat.id,
                             text=f"режим изменен на {call.data} введите угол и тригонометрическую фукнцию через запятую и пробел")
        return 1          
    else:
        bot.send_message(chat_id=call.message.chat.id,
             text=f"режим изменен на {call.data}, введите функцию, которая будет интегрирована, а также нижний и верхний пределы через пробелы")
        return 1

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
            return bot.send_message(chat_id=message.chat.id, text="введите 3 числа")
        try:
            kf = list(map(float, kf))
        except Exception:
            return bot.send_message(chat_id=message.chat.id, text="введите числа")
        if kf[0] == 0 or kf[1] == 0 or kf[2] == 0:
            return bot.send_message(chat_id=message.chat.id, text="коэффицент не должен быть равен нулю")

        a, b, c = kf
        D = int(b ** 2) - (4 * a * c)

        x = np.arange(-10, 10, 0.1)
        y = a*x**2 + b*x + c
        plt.plot(x,y)
        plt.title('Quadratic Function')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('quadratic.png')
    
        if D < 0:
            x1 = round_complex((-b + cmath.sqrt(D)) / (2*a))
            x2 = round_complex((-b - cmath.sqrt(D)) / (2*a))    
            bot.send_message(chat_id=message.chat.id, text=f"Нет вещественных корней, но есть комплексные:  \
                \n\nПервый корень = {x1}\nВторой корень = {x2}")
            bot.send_photo(chat_id=message.chat.id, photo=open('quadratic.png', 'rb'))
            return 1
        if D == 0:
            x = -b / 2 * a
            bot.send_message(chat_id=message.chat.id, text=f"один корень: {int(x)}")
            bot.send_photo(chat_id=message.chat.id, photo=open('quadratic.png', 'rb'))
            return 1

        x1: float = (-b - D ** 0.5) / (2 * a)
        x2: float = (-b + D ** 0.5) / (2 * a)

        if str(x1).endswith('.0'):
            x1 = int(x1)
        if str(x2).endswith('.0'):
            x2 = int(x2)    
        bot.send_message(chat_id=message.chat.id, text=f'Дискриминант = *{D}*\n\n *Корни:*\nПервый корень = {format(x1,".3f")}\nВторой корень = {format(x2, ".3f")}', parse_mode='Markdown')
        bot.send_photo(chat_id=message.chat.id, photo=open('quadratic.png', 'rb'))
        return 1

    elif current_state == 'trigonometry':
        text = message.text.split(", ")
        if len(text) != 2:
            return bot.send_message(chat_id=message.chat.id, text=f'введите "угол, функция"')
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

        bot.send_message(chat_id=message.chat.id, text=f"{trig_function}(x) = {format(result, '.1f')}")   
        return 1
    
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

    if current_state == 'cubic':
        text = message.text
        kf = text.split()
        if len(kf) != 4:
            return bot.send_message(chat_id=message.chat.id, text="введите 4 числа")
        try:
            kf = list(map(float, kf))
        except Exception:
            return bot.send_message(chat_id=message.chat.id, text="введите числа")
        if kf[0] == 0 or kf[1] == 0 or kf[2] == 0:
            return bot.send_message(chat_id=message.chat.id, text="коэффицент не должен быть равен нулю")

        a, b, c, d= kf
        p = b - a**2 / 3
        q = 2 * a**3 / 27 - a * b / 3 + c
        r = cmath.sqrt(-q/2 + cmath.sqrt(q**2/4 + p**3/27))
        s = cmath.sqrt(-q/2 - cmath.sqrt(q**2/4 + p**3/27))

        # x = np.arange(-10, 10, 0.1)
        # y = a*x**3 + b*x**2 + c*x + d
        # plt.plot(x,y)
        # plt.title('Quadratic Function')
        # plt.xlabel('x')
        # plt.ylabel('y')
        # plt.savefig('cubic.png')
    
        x1 = r + s - a/3
        x2 = -(r + s)/2 - a/3 + math.sqrt(3)/2 * (r - s) * 1j
        x3 = -(r + s)/2 - a/3 - math.sqrt(3)/2 * (r - s) * 1j
        bot.send_message(chat_id=message.chat.id, text=f'*Корни:*\nПервый корень = {format(x1,".3f")}\nВторой корень = {format(x2, ".3f")}\nТретий корень = {format(x3,".3f")}', parse_mode='Markdown')
        # bot.send_photo(chat_id=message.chat.id, photo=open('cubic.png', 'rb'))
        return 1

    if current_state == 'quartic':
        text = message.text
        kf = text.split()
        if len(kf) != 5:
            return bot.send_message(chat_id=message.chat.id, text="введите 5 чисел")
        try:
            kf = list(map(float, kf))
        except Exception:
            return bot.send_message(chat_id=message.chat.id, text="введите числа")
        if kf[0] == 0 or kf[1] == 0 or kf[2] == 0:
            return bot.send_message(chat_id=message.chat.id, text="коэффицент не должен быть равен нулю")

        a, b, c, d, e= kf
        p = 8 * b - 3 * a**2
        q = a**3 - 4 * a * b + 8 * c
        r = cmath.sqrt(-q/2 + cmath.sqrt(q**2/4 + p**3/27))
        s = cmath.sqrt(-q/2 - cmath.sqrt(q**2/4 + p**3/27))

        x = np.arange(-10, 10, 0.1)
        y = a*x**4 + b*x**3 + c*x*2 + d*x + e
        plt.plot(x,y)
        plt.title('Quadratic Function')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('quartic.png')
    
        u = r + s
        v = math.sqrt(3) * (r - s)
    
        x1 = cmath.sqrt(-a/4 + u/2 + v/2) + cmath.sqrt(-a/4 + u/2 - v/2)
        x2 = cmath.sqrt(-a/4 + u/2 + v/2) - cmath.sqrt(-a/4 + u/2 - v/2)
        x3 = -cmath.sqrt(-a/4 + u/2 + v/2) + cmath.sqrt(-a/4 + u/2 - v/2) * 1j
        x4 = -cmath.sqrt(-a/4 + u/2 + v/2) - cmath.sqrt(-a/4 + u/2 - v/2) * 1j

        bot.send_message(chat_id=message.chat.id,
            text=f'*Корни:*\nПервый корень = {format(x1,".3f")}\nВторой корень = {format(x2, ".3f")}\nТретий корень = {format(x3,".3f")}\nЧетвёртый корень = {format(x4,".3f")}',\
                 parse_mode='Markdown')
        bot.send_photo(chat_id=message.chat.id, photo=open('quartic.png', 'rb'))
        return 1


    else:
            return bot.send_message(chat_id=message.chat.id, text="Неверно")
    # except:
    #     pass
    # return 1

bot.polling(non_stop=True)
    
plt.ioff() #отключение интерактивного режима matplotlib

