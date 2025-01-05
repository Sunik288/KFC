import telebot

import buttons as btn
import database as db


bot = telebot.TeleBot('7741048536:AAHLCcN_WzyXHphIfZb356f_eMdmArRbwwg')
admin_group = -4753465855

users = {}

# db.add_product("Burger", 30000.00, 10, 'The best burger', "https://www.gazeta.uz/media/img/2017/10/8NWCAY15072899796600_l.jpg")
# db.add_product("Cheeseburger", 35000.00, 10, 'The best cheeseburger', "https://www.gazeta.uz/media/img/2017/10/8NWCAY15072899796600_l.jpg")
# db.add_product("Hotdog", 25000.00, 0, 'The best hotdog', "https://www.gazeta.uz/media/img/2017/10/8NWCAY15072899796600_l.jpg")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in db.list_id:
        bot.send_message(user_id, 'Welcome to KFC bot!')
        bot.send_message(user_id, 'Please send your name☺️')
        bot.register_next_step_handler(message, name)
    else:
        bot.send_message(user_id, 'Choose from the navigation bar below👇', reply_markup=btn.main())


def name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Great! Now send your phone number', reply_markup=btn.phone())
    bot.register_next_step_handler(message, phone, user_name)

def phone(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        db.add_user(user_id, user_name, phone_number)
        bot.send_message(user_id, 'You have successfully finished the registration', reply_markup= telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Choose from the navigation bar below👇', reply_markup=btn.main())
    else:
        bot.send_message(user_id, 'Please send your phone number using the button below👇', reply_markup=btn.phone())
        bot.register_next_step_handler(message, phone, user_name)

@bot.message_handler(content_types=['text'])
def main_bar(message):
    user_id = message.from_user.id
    if message.text == 'Review✍️':
        bot.send_message(user_id, 'Please send your review!')
        bot.register_next_step_handler(message, review)
    elif message.text == 'Menu🍴':
        all_products = db.pr_id_name()
        bot.send_message(user_id, 'What do you want to order?', reply_markup=btn.menu(all_products))
    elif message.text == 'Cart🛒':
        first = 'Your cart: '
        full_text = ''

        cart_info = db.get_exact_cart(user_id)
        count = 1
        total = 0

        for i in cart_info:
            full_text += f'{count}. {i[0]} X {i[1]} = {i[2]} UZS\n'
            total += i[2]
            count += 1

        full_text += f'Total: {total} UZS'

        products = db.get_cart_id_name(user_id)

        bot.send_message(user_id, first)
        bot.send_message(user_id, full_text, reply_markup=btn.cart(products))



def review(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Thank you for your review🤗', reply_markup=btn.main())
    bot.send_message(admin_group, f'Review:{message.text}\nUser id: {user_id}')

@bot.callback_query_handler(lambda call: 'prod_' in call.data)
def product(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    pr_id = int(call.data.replace('prod_', ''))
    pr_info = db.get_exact_product(pr_id)

    users[user_id] = {
        'pr_id': pr_id,
        'pr_name': pr_info[0],
        'pr_price': pr_info[1],
        'pr_count': 1
    }


    bot.send_photo(user_id, photo=f'{pr_info[3]}', caption=f'{pr_info[0]}\n\nPrice: {pr_info[1]}\nDescription: {pr_info[2]}'
                   , reply_markup=btn.product_menu())

@bot.callback_query_handler(lambda call: call.data in ['back', 'plus', 'minus', 'back_menu', 'to_cart', 'cart', 'clear', 'order', 'back_cart'])
def operations(call):
    user_id = call.message.chat.id
    if call.data == 'back':
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, 'Choose from the navigation bar below👇', reply_markup=btn.main())

    elif call.data == 'back_cart':
        bot.delete_message(user_id, call.message.message_id-1)
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, 'Choose from the navigation bar below👇', reply_markup=btn.main())

    elif call.data == 'plus':
        current_amount = users[user_id]['pr_count']
        users[user_id]['pr_count'] += 1
        available_quan = db.get_exact_product_quantity(users[user_id]['pr_id'])
        if current_amount + 1 <= available_quan:
            bot.edit_message_reply_markup(user_id, call.message.id, reply_markup=btn.product_menu(plus_or_minus='plus',
                                                                                                  current_amount=current_amount))
        else:
            bot.send_message(user_id, 'The product amount exceeds the limit')


    elif call.data == 'minus':
        current_amount = users[user_id]['pr_count']
        users[user_id]['pr_count'] -= 1
        bot.edit_message_reply_markup(user_id, call.message.id,
                                      reply_markup=btn.product_menu(plus_or_minus='minus', current_amount=current_amount))

    elif call.data == 'back_menu':
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.pr_id_name()
        bot.send_message(user_id, 'What do you want to order?', reply_markup=btn.menu(all_products))

    elif call.data == 'to_cart':
        db.add_to_cart(user_id, users[user_id]['pr_id'], users[user_id]['pr_name'], users[user_id]['pr_count'], users[user_id]['pr_price'])
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.pr_id_name()
        bot.send_message(user_id, 'What do you want to order?', reply_markup=btn.menu(all_products))

    elif call.data == 'cart':
        bot.delete_message(user_id, call.message.message_id)
        first = 'Your cart: '
        full_text = ''

        cart_info = db.get_exact_cart(user_id)
        count = 1
        total = 0

        for i in cart_info:
            full_text += f'{count}. {i[0]} X {i[1]} = {i[2]} UZS\n'
            total += i[2]
            count+=1

        full_text += f'Total: {total} UZS'

        products = db.get_cart_id_name(user_id)

        bot.send_message(user_id, first)
        bot.send_message(user_id, full_text, reply_markup=btn.cart(products))

    elif call.data == 'clear':
        db.delete_exact_cart(user_id)
        full_text = ''

        cart_info = db.get_exact_cart(user_id)
        count = 1
        total = 0

        for i in cart_info:
            full_text += f'{count}. {i[0]} X {i[1]} = {i[2]} UZS\n'
            total += i[2]
            count+=1

        full_text += f'Total: {total} UZS'
        bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=f'{full_text}', reply_markup=btn.empty_cart())

    elif call.data == 'order':
        cart_info = db.get_exact_cart(user_id)
        db.delete_exact_cart(user_id)
        bot.delete_message(user_id, call.message.message_id)

        full_text = f'New order!\nUser id: {user_id}\n\n'


        count = 1
        total = 0

        for i in cart_info:
            full_text += f'{count}. {i[0]} X {i[1]} = {i[2]} UZS\n'
            db.order(i[3], i[1])
            total += i[2]
            count += 1

        full_text += f'Total: {total} UZS'

        bot.send_message(admin_group, full_text)
        all_products = db.pr_id_name()
        bot.send_message(user_id, 'Your order has been placed. Do you want to order something more?', reply_markup=btn.menu(all_products))



@bot.callback_query_handler(lambda call: 'delete_' in call.data)
def delete(call):
    user_id = call.message.chat.id
    pr_id = int(call.data.replace('delete_', ''))
    db.delete_exact_product_from_cart(user_id, pr_id)
    full_text = ''

    cart_info = db.get_exact_cart(user_id)
    count = 1
    total = 0

    for i in cart_info:
        full_text += f'{count}. {i[0]} X {i[1]} = {i[2]} UZS\n'
        total += i[2]
        count += 1

    full_text += f'Total: {total} UZS'
    products = db.get_cart_id_name(user_id)

    if total != 0:
        bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=f'{full_text}',
                              reply_markup=btn.cart(products))
    else:
        bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=f'{full_text}',
                              reply_markup=btn.empty_cart())






bot.infinity_polling()