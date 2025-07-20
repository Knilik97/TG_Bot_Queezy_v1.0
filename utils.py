#Вспомогательные функции для создания интерфейсов и обработки результатов:

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def generate_options_keyboard(options, correct_answer):
    """Генерирует inline-клавиатуру с вариантами ответов"""
    builder = InlineKeyboardBuilder()
    for i, opt in enumerate(options):
        cb_data = f"{i}"  # Данные кнопки: номер варианта
        builder.button(text=opt, callback_data=cb_data)
    builder.adjust(1)
    return builder.as_markup()

async def show_stats(dp):
    top_users = await dp.get_top_results()
    msg = "Топ игроков:\n\n"
    for idx, (user_id, score) in enumerate(top_users):
        msg += f"{idx + 1}. Пользователь ID:{user_id}, лучший результат: {score}\n"
    await dp.bot.send_message(chat_id=-1, text=msg)  # Отправляем статистику админам или в группу (-1 заменяется на реальный чат)