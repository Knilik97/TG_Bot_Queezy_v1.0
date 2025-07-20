#Хендлеры для основных действий пользователя:

from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import API_TOKEN
from questions import quiz_data
from db_manager import *
from utils import generate_options_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await insert_or_update_user(message.from_user.id)
    await message.answer("Привет! Нажмите \"Начать игру\", чтобы начать.",
                         reply_markup={"keyboard": [[{"text": "Начать игру"}]], "resize_keyboard": True})


@router.message(F.text.lower().contains("начать игру"))
async def begin_game(message: Message):
    index = await get_quiz_index(message.from_user.id)
    question = quiz_data[index]["question"]
    options = quiz_data[index]["options"]
    keyboard = generate_options_keyboard(options, quiz_data[index]["correct_option"])
    await message.answer(question, reply_markup=keyboard)


@router.callback_query(lambda c: c.data.isdigit())
async def handle_answer(callback: CallbackQuery):
    selected_option = int(callback.data)

    # Получаем индекс текущего вопроса
    index = await get_quiz_index(callback.from_user.id)

    # Берём данные текущего вопроса
    correct_option = quiz_data[index]['correct_option']

    if selected_option == correct_option:
        await callback.message.answer("Правильно!")
    else:
        await callback.message.answer(
            f"Неверно. Правильный ответ: {quiz_data[index]['options'][correct_option]}"
        )

    # Удаляем клавиатуру
    await callback.message.delete_reply_markup()

    # Переходим к следующему вопросу
    next_idx = index + 1
    await update_quiz_index(callback.from_user.id, next_idx)

    if next_idx >= len(quiz_data):
        await callback.message.answer("Поздравляю! Вы завершили тест.")
    else:
        await begin_game(callback.message)
