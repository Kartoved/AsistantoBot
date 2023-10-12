"""хендлеры"""

from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
)
from aiogram.filters import Command, BaseFilter
from config_data.config import bot
import services.services as s
from random import choice
from datetime import datetime

router: Router = Router()

admin_ids: list[int] = s.import_ids()


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


@router.message(Command(commands=["start"]), IsAdmin(admin_ids))
async def process_start_command(message: Message):
    """запуск бота, создание необходимых файлов"""
    pass


# продукты
@router.message(F.text.startswith("купить"), IsAdmin(admin_ids))
async def add_product(message: Message):
    """добавление продукта в список продуктов"""
    s.add_product(text=message.text)
    products_list = s.import_products_list()
    keyboard = s.create_inline_kbP(1, *products_list)
    for user in admin_ids:
        await bot.send_message(
            chat_id=user, text=f"➕ Продукты добавлены:\n{message.text[7::]}")
        await bot.send_message(
            chat_id=user, text="🛒 Ваш список продуктов:", reply_markup=keyboard)


@router.message(Command(commands=["show_products"]), IsAdmin(admin_ids))
async def show_products_list(message: Message):
    """показать список продуктов"""
    products_list = s.import_products_list()
    keyboard = s.create_inline_kbP(1, *products_list)
    await message.answer(text="🛒 Ваш список продуктов:", reply_markup=keyboard)


# кайфы
@router.message(F.text.startswith("кайфы"), IsAdmin(admin_ids))
async def add_joy(message: Message):
    """добавление кайфов в список кайфов"""
    s.add_joy(text=message.text)
    joys_list = s.import_joys_list()
    joys_string: str = ""
    for joy in joys_list:
        joys_string += f"\n{joys_list.index(joy)+1}) {joy}"
    for user in admin_ids:
        await bot.send_message(
            chat_id=user, text=f"➕ Кайфы добавлены:\n{message.text[6::]}"
        )
        await bot.send_message(chat_id=user, text=f"📋 Ваш список кайфов: {joys_string}")


@router.message(F.text(startswith={"выполнить"}, ignore_case=True), IsAdmin(admin_ids))
async def done_joy(message: Message):
    joys_list = s.import_joys_list()
    new_completed_joys = message.text.split("\n")
    new_completed_joys.remove("выполнить")
    new_joys = {}
    ratio = 1
    joys_string: str = ""
    for joy in new_completed_joys:
        try:
            new_joys[joys_list[int(joy) - ratio]] = datetime.now().strftime("%d/%m/%Y")
            joys_string += f"- {joys_list.pop(int(joy)-ratio)}\n"
            ratio += 1
        except IndexError:
            pass
    completed_joys = s.import_completed_joys()
    s.export_joys_list(joys_list)
    s.export_completed_joys(completed_joys | new_joys)
    for user in admin_ids:
        await bot.send_message(chat_id=user, text=f"✅ Выполнено:\n{joys_string}")


@router.message(Command(commands=["show_joys"]), IsAdmin(admin_ids))
async def show_joys_list(message: Message):
    """показать список продуктов"""
    joys_list: list = s.import_joys_list()
    joys_string: str = ""
    for joy in joys_list:
        joys_string += f"\n{joys_list.index(joy)+1}) {joy}"
    await message.answer(text=f"📋 Ваш список кайфов: {joys_string}")


@router.message(Command(commands=["show_completed_joys"]), IsAdmin(admin_ids))
async def show_completed_joys(message: Message):
    """показать список выполненных кайфов"""
    completed_joys: list = list(s.import_completed_joys())
    joys_string: str = ""
    for joy in completed_joys:
        joys_string += f"{completed_joys.index(joy)+1}) {joy}\n"
    await message.answer(
        text=f"✅ Всего выполнено кайфов: \
<em>{len(completed_joys)}/{len(completed_joys+s.import_joys_list())}</em>\
        \n\nВаш список выполненных кайфов:\n{joys_string}"
    )


@router.message(Command(commands=["get_random_joy"]), IsAdmin(admin_ids))
async def get_random_joy(message: Message):
    """получить один рандомный кайф"""
    joys_list = s.import_joys_list()
    try:
        await message.answer(
            text=f"🎲 Случайное кайфовое дело на сегодня:\n{choice(joys_list)}"
        )
    except IndexError:
        await message.answer(text="Список кайфов пуст")


@router.inline_query()
async def inline_x(inline_query: InlineQuery) -> None:
    text = inline_query.query
    input_contet = InputTextMessageContent
