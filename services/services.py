'''вспомогательные функции'''

import json
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def import_ids():
    '''импортирует айдишники пользователей, которые могут юзать бота'''
    with open('user_info/ids.json') as f:
        ids: list = json.load(f)
        return ids


def create_inline_kbP(width: int,
                      *kwargs: str) -> InlineKeyboardMarkup:
    '''создаёт клавиатуру с продуктами'''
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for button in kwargs:
        if button != '\n':
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=f'{button}delP'))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()

# продукты


def import_products_list() -> list:
    '''импортирует список продуктов из файла'''
    with open('user_info/produсt_list.json') as f:
        products_list: list = json.load(f)
        return products_list


def export_products_list(products_list, new_products=''):
    '''экспортирует список продуктов в json'''
    with open('user_info/produсt_list.json', 'w') as f:
        products_list += new_products
        json.dump(list(set(products_list)), f, ensure_ascii=False)


def add_product(text: str):
    '''добавляет продукт в список подуктов'''
    products_list: list = import_products_list()
    new_products: list = text.split('\n')
    try:
        new_products.remove('Продукты')
    except ValueError:
        new_products.remove('продукты')
    export_products_list(products_list, new_products)


def buy_product(product: str) -> list:
    '''удаляет продукт из списка'''
    products_list: list = import_products_list()
    products_list.remove(product)
    export_products_list(products_list)
    return products_list


# кайфы

def create_inline_kbJ(width: int,
                      *kwargs: str) -> InlineKeyboardMarkup:
    '''создаёт клавиатуру с продуктами'''
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for button in kwargs:
        if button != '\n':
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=f'{button}delJ'))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


def import_joys_list() -> list:
    '''импортирует список кайфов из файла'''
    with open('user_info/summer_joys.json') as f:
        summer_joys: list = json.load(f)
        return summer_joys


def export_joys_list(summer_joys, new_joy=''):
    '''экспортирует список кайфов в json'''
    with open('user_info/summer_joys.json', 'w') as f:
        summer_joys += new_joy
        json.dump(list(set(summer_joys)), f, ensure_ascii=False)


def import_completed_joys() -> str:
    with open('user_info/completed_joys.txt') as f:
        completed_joys = f.read()
    return completed_joys


def export_comleted_joys(completed_joy: str):
    with open('user_info/completed_joys.txt', 'a') as f:
        f.write(f'✅ {completed_joy}\n')


def add_joy(text: str):
    '''добавляет кайфы в список кайфов'''
    summer_joys: list = import_joys_list()
    new_joys: list = text.split('\n')
    try:
        new_joys.remove('Кайфы')
    except ValueError:
        new_joys.remove('кайфы')
    export_joys_list(summer_joys, new_joys)


def completed_joys(joy: str) -> list:
    '''выполненный кайф'''
    summer_joys: list = import_joys_list()
    summer_joys.remove(joy)
    export_joys_list(summer_joys)
    return summer_joys
