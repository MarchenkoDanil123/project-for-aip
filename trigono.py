import telebot, sys

from telebot import types

bot = telebot.TeleBot("5780902069:AAEilKTdKOQJJcB8EvJ1u9rt9skgwv_J2yw")

A11 = ''
A12 = ''
A13 = ''
A14 = ''
A15 = ''

A21 = ''
A22 = ''
A23 = ''
A24 = ''
A25 = ''

A31 = ''
A32 = ''
A33 = ''
A34 = ''
A35 = ''

A41 = ''
A42 = ''
A43 = ''
A44 = ''
A45 = ''

A51 = ''
A52 = ''
A53 = ''
A54 = ''
A55 = ''

A112 = ''
A122 = ''
A132 = ''
A142 = ''
A152 = ''

A212 = ''
A222 = ''
A232 = ''
A242 = ''
A252 = ''

A312 = ''
A322 = ''
A332 = ''
A342 = ''
A352 = ''

result = None
result2 = None


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("2x2")
    btn2 = types.KeyboardButton("3x3")
    btn3 = types.KeyboardButton("4x4")
    btn4 = types.KeyboardButton("5x5")
    markup.add(btn1, btn2, btn3, btn4)
    send_mess = f"<b>Hello, {message.from_user.first_name} {message.from_user.last_name}!\nPlease choose with what matrix you need help)</b>"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global msg
    if (message.text == "2x2"):
        msg = bot.send_message(message.chat.id, text="Ok, you choose 2x2, please write A11)")
        bot.register_next_step_handler(msg, process_A11)
    elif(message.text == "3x3"):
        msg = bot.send_message(message.chat.id, "Ok, you choose 3x3, plz write A11")
        bot.register_next_step_handler(msg, process2_A11)



def process_A11(message, result=None):
    global A11

    if result == None:
        A11 = int(message.text)
    else:
        A11 = str(result)

    msg = bot.send_message(message.chat.id, "Nice, now A12")
    bot.register_next_step_handler(msg, process_A12)


def process_A12(message):
    global A12

    A12 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A21")
    bot.register_next_step_handler(msg, process_A21)


def process_A21(message):
    global A21

    A21 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A22")
    bot.register_next_step_handler(msg, process_A22)


def calc2x2():
    global A11, A12, A21, A22, result

    result = str(A11 * A22 - A12 * A21)

    return result


def process_A22(message):
    global A22

    A22 = int(message.text)

    msg = bot.send_message(message.chat.id, "Your result is: " + calc2x2())


def process2_A11(message, result2=None):
    global A112

    if result2 == None:
        A112 = int(message.text)
    else:
        A112 = str(result2)

        bot.send_message(message.chat.id, "Nice, now A12")
        process2_A12(message)

def process2_A12(message):
    global A122

    A122 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A13")
    bot.register_next_step_handler(msg, process2_A13)


def process2_A13(message):
    global A132

    A132 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A21")
    bot.register_next_step_handler(msg, process2_A21)

def process2_A21(message):
    global A212

    A212 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A22")
    bot.register_next_step_handler(msg, process2_A22)


def process2_A22(message):
    global A222

    A222 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A23")
    bot.register_next_step_handler(msg, process2_A23)

def process2_A23(message):
    global A232

    A232 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A31")
    bot.register_next_step_handler(msg, process2_A31)

def process2_A31(message):
    global A312

    A312 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A32")
    bot.register_next_step_handler(msg, process2_A32)

def process2_A32(message):
    global A322

    A322 = int(message.text)

    msg = bot.send_message(message.chat.id, "now A33")
    bot.register_next_step_handler(msg, process2_A33)


def calc3x3():
    global A112, A122, A132, A212, A222, A232, A312, A322, A332, result2

    result2 = str(A112*A222*A332+A212*A322*A132+A312*A122*A232-A132*A222*A312-A232*A322*A112-A332*A122*A212)

    return result2

def process2_A33(message):
    global A332

    A332 = int(message.text)

    msg = bot.send_message(message.chat.id, "Your result is: " + calc3x3())

bot.polling(none_stop=True)








import math

def solve_cubic(a, b, c):
    p = b - a**2 / 3
    q = 2 * a**3 / 27 - a * b / 3 + c
    r = math.sqrt(-q/2 + math.sqrt(q**2/4 + p**3/27))
    s = math.sqrt(-q/2 - math.sqrt(q**2/4 + p**3/27))
    
    x1 = r + s - a/3
    x2 = -(r + s)/2 - a/3 + math.sqrt(3)/2 * (r - s) * 1j
    x3 = -(r + s)/2 - a/3 - math.sqrt(3)/2 * (r - s) * 1j
    
    return x1, x2, x3

# Solve the equation x^3 + 2x^2 + 3x + 4 = 0
roots = solve_cubic(2, 3, 4)
print(roots)


import math

def solve_quartic(a, b, c, d):
    p = 8 * b - 3 * a**2
    q = a**3 - 4 * a * b + 8 * c
    r = math.sqrt(-q/2 + math.sqrt(q**2/4 + p**3/27))
    s = math.sqrt(-q/2 - math.sqrt(q**2/4 + p**3/27))
    
    u = r + s
    v = math.sqrt(3) * (r - s)
    
    x1 = math.sqrt(-a/4 + u/2 + v/2) + math.sqrt(-a/4 + u/2 - v/2)
    x2 = math.sqrt(-a/4 + u/2 + v/2) - math.sqrt(-a/4 + u/2 - v/2)
    x3 = -math.sqrt(-a/4 + u/2 + v/2) + math.sqrt(-a/4 + u/2 - v/2) * 1j
    x4 = -math.sqrt(-a/4 + u/2 + v/2) - math.sqrt(-a/4 + u/2 - v/2) * 1j
    
    return x1, x2, x3, x4

# Solve the equation x^4 + 3x^3 + 2x^2 + 4x + 1 = 0
roots = solve_quartic(3, 2, 4, 1)
print(roots)
