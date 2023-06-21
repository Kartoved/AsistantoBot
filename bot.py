'''исполняемый файл'''

import asyncio
from aiogram import Dispatcher
from config_data.config import bot
from handlers import user_handlers
from lexicon import callbacks
from keyboards.set_main_menu import set_main_menu


async def main():
    dp: Dispatcher = Dispatcher()
    # await bot.delete_my_commands()
    dp.startup.register(set_main_menu)
    dp.include_router(user_handlers.router)
    dp.include_router(callbacks.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
