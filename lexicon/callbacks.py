'''коллбэки'''

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, BaseFilter
import services.services as s

router = Router()

admin_ids: list[int] = s.import_ids()


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


@router.callback_query(Text(endswith=['delP']), IsAdmin(admin_ids))
async def delete_product(callback: CallbackQuery):
    '''удаление продукта из списка при нажатии на кнопку'''
    await callback.answer(text=f'✅ {callback.data[:-4]} купили')
    products_list = s.buy_product(callback.data[:-4])
    keyboard = s.create_inline_kbP(3, *products_list)
    await callback.message.edit_text(text='🛒 Ваш список продуктов:',
                                     reply_markup=keyboard)


@router.callback_query(Text(endswith=['delJ']), IsAdmin(admin_ids))
async def done(callback: CallbackQuery):
    '''удаление продукта из списка при нажатии на кнопку'''
    await callback.answer(text=f'✅ {callback.data[:-4]} выполнено!')
    joys_list = s.completed_joys(callback.data[:-4])
    keyboard = s.create_inline_kbJ(3, *joys_list)
    s.export_comleted_joys(callback.data[:-4])
    await callback.message.edit_text(text='🥳 Ваш список кайфов:',
                                     reply_markup=keyboard)
