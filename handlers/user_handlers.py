'''хендлеры'''

from aiogram import Router
from aiogram.types import Message, InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.filters import Command, Text, BaseFilter
from config_data.config import bot
import services.services as s
from random import choice

router: Router = Router()

admin_ids: list[int] = s.import_ids()


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


@router.message(Command(commands=['start']), IsAdmin(admin_ids))
async def process_start_command(message: Message):
    '''запуск бота, создание необходимых файлов'''
    pass


# продукты
@router.message(Text(startswith={'продукты'}, ignore_case=True), IsAdmin(admin_ids))
async def add_product(message: Message):
    '''добавление продукта в список продуктов'''
    s.add_product(text=message.text)
    products_list = s.import_products_list()
    keyboard = s.create_inline_kbP(3, *products_list)
    for user in admin_ids:
        await bot.send_message(chat_id=user,
                               text=f'➕ Продукты добавлены:\n{message.text[9::]}')
        await bot.send_message(chat_id=user,
                               text='🛒 Ваш список продуктов:',
                               reply_markup=keyboard)


@router.message(Command(commands=['show_products']), IsAdmin(admin_ids))
async def show_products_list(message: Message):
    '''показать список продуктов'''
    products_list = s.import_products_list()
    keyboard = s.create_inline_kbP(3, *products_list)
    await message.answer(text='🛒 Ваш список продуктов:',
                         reply_markup=keyboard)


# кайфы
@router.message(Text(startswith={'кайфы'}, ignore_case=True), IsAdmin(admin_ids))
async def add_joy(message: Message):
    '''добавление кайфов в список кайфов'''
    s.add_joy(text=message.text)
    joys_list = s.import_joys_list()
    keyboard = s.create_inline_kbJ(1, *joys_list)
    for user in admin_ids:
        await bot.send_message(chat_id=user,
                               text=f'➕ Кайфы добавлены:\n{message.text[6::]}')
        await bot.send_message(chat_id=user,
                               text='📋 Ваш список кайфов:',
                               reply_markup=keyboard)


@router.message(Command(commands=['show_joys']), IsAdmin(admin_ids))
async def show_joys_list(message: Message):
    '''показать список продуктов'''
    joys_list = s.import_joys_list()
    keyboard = s.create_inline_kbJ(3, *joys_list)
    await message.answer(text='📋  Ваш список кайфов:',
                         reply_markup=keyboard)


@router.message(Command(commands=['show_completed_joys']), IsAdmin(admin_ids))
async def show_completed_joys(message: Message):
    '''показать список выполненных кайфов'''
    joys_list = s.import_completed_joys()
    await message.answer(text=f'🥳 Ваш список выполненных кайфов:\n{joys_list}')


@router.message(Command(commands=['get_random_joy']), IsAdmin(admin_ids))
async def get_random_joy(message: Message):
    '''получить один рандомный кайф'''
    joys_list = s.import_joys_list()
    await message.answer(text=f'📆 Случайное кайфовое дело на сегодня:\n{choice(joys_list)}')


@router.inline_query()
async def inline_x(inline_query: InlineQuery) -> None:
    text = inline_query.query
    input_contet = InputTextMessageContent
