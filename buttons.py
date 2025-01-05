from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def phone():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = KeyboardButton('Send phone number', request_contact=True)

    kb.add(item1)

    return kb

def main():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = KeyboardButton(text='Menu🍴')
    item2 = KeyboardButton(text='Review✍️')
    item3 = KeyboardButton(text='Cart🛒')

    kb.row(item1)
    kb.row(item2, item3)

    return kb

def menu(all_products):

    kb = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(text='Back⬅️', callback_data='back')
    item2 = InlineKeyboardButton(text='Cart🛒', callback_data='cart')

    item3 = [InlineKeyboardButton(text=f'{product[1]}', callback_data=f'prod_{product[0]}') for product in all_products]

    kb.add(*item3)
    kb.row(item2)
    kb.row(item1)

    return kb

def product_menu(plus_or_minus='', current_amount=1):

    kb = InlineKeyboardMarkup(row_width=3)

    item1 = InlineKeyboardButton('➕', callback_data='plus')
    item2 = InlineKeyboardButton(text=f'{current_amount}', callback_data='none')
    item3 = InlineKeyboardButton('➖', callback_data='minus')

    if plus_or_minus == 'plus':
        item2 = InlineKeyboardButton(text=f'{current_amount + 1}', callback_data='none')


    elif plus_or_minus == 'minus':
        if current_amount > 1:
            item2 = InlineKeyboardButton(text=f'{current_amount - 1}', callback_data='none')

    item5 = InlineKeyboardButton(text='Back⬅️', callback_data='back_cart')
    item4 = InlineKeyboardButton(text='Add to cart🛒', callback_data='to_cart')

    kb.row(item1, item2, item3)
    kb.row(item4)
    kb.row(item5)

    return kb

def cart(cart_products):
    kb = InlineKeyboardMarkup(row_width=2)

    item1 = [InlineKeyboardButton(text=f'{product[1]} ❌', callback_data=f'delete_{product[0]}') for product in cart_products]
    item3 = InlineKeyboardButton(text='Back⬅️', callback_data='back_menu')
    item2 = InlineKeyboardButton(text='Order✅', callback_data='order')
    item4 = InlineKeyboardButton(text='Clear cart🛒', callback_data='clear')

    kb.add(*item1)
    kb.row(item2)
    kb.row(item4)
    kb.row(item3)

    return kb

def empty_cart():
    kb = InlineKeyboardMarkup(row_width=1)

    item3 = InlineKeyboardButton(text='Back⬅️', callback_data='back_menu')
    kb.row(item3)

    return kb
