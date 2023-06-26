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
    with open('user_info/joys.json') as f:
        joys: list = json.load(f)
        return joys


def export_joys_list(joys, new_joy=''):
    '''экспортирует список кайфов в json'''
    with open('user_info/joys.json', 'w') as f:
        joys += new_joy
        json.dump(sorted(list(set(joys))), f, ensure_ascii=False)


def import_completed_joys() -> str:
    with open('user_info/completed_joys.json') as f:
        completed_joys = json.load(f)
    return completed_joys


def export_completed_joys(completed_joys: list):
    with open('user_info/completed_joys.json', 'w') as f:
        json.dump(completed_joys, f, ensure_ascii=False)


def add_joy(text: str):
    '''добавляет кайфы в список кайфов'''
    joys: list = import_joys_list()
    new_joys: list = text.split('\n')
    try:
        new_joys.remove('Кайфы')
    except ValueError:
        new_joys.remove('кайфы')
    export_joys_list(joys, new_joys)


def completed_joys(joy: str) -> list:
    '''выполненный кайф'''
    joys: list = import_joys_list()
    joys.remove(joy)
    export_joys_list(joys)
    return joys
