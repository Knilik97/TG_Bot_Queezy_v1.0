#Работа с базой данных SQLite:

import sqlite3
import aiosqlite
import config

async def create_tables():
    async with aiosqlite.connect(config.DB_NAME) as conn:
        cursor = await conn.cursor()
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                current_question INTEGER DEFAULT 0
            );
        ''')
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                score INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        ''')
        await conn.commit()


async def insert_or_update_user(user_id):
    async with aiosqlite.connect(config.DB_NAME) as conn:
        cursor = await conn.cursor()
        result = await cursor.execute('SELECT * FROM users WHERE user_id=?;', (user_id,))
        row = await result.fetchone()
        if not row:
            await cursor.execute('INSERT INTO users VALUES (?, ?);', (user_id, 0))
        await conn.commit()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(config.DB_NAME) as conn:
        cursor = await conn.cursor()
        result = await cursor.execute('SELECT current_question FROM users WHERE user_id=?;', (user_id,))
        row = await result.fetchone()
        return row[0] if row else None


async def update_quiz_index(user_id, new_index):
    async with aiosqlite.connect(config.DB_NAME) as conn:
        cursor = await conn.cursor()
        await cursor.execute('UPDATE users SET current_question=? WHERE user_id=?;', (new_index, user_id))
        await conn.commit()


async def save_result(user_id, score):
    async with aiosqlite.connect(config.DB_NAME) as conn:
        cursor = await conn.cursor()
        await cursor.execute('INSERT INTO results (user_id, score) VALUES (?, ?)', (user_id, score))
        await conn.commit()


async def get_top_results(limit=5):
    async with aiosqlite.connect(config.DB_NAME) as conn:
        cursor = await conn.cursor()
        result = await cursor.execute('SELECT user_id, MAX(score) AS max_score '
                                     'FROM results GROUP BY user_id ORDER BY max_score DESC LIMIT ?', (limit,))
        rows = await result.fetchall()
        return [(row[0], row[1]) for row in rows]