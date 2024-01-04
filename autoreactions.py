from pyrogram import Client, filters
from helps.modules import add_module, add_command
from helps.scripts import get_keys, set_key
import asyncio
import random
from main import c, conn

from helps.get_prefix import get_prefix
prefix = get_prefix()

c.execute('''
        CREATE TABLE IF NOT EXISTS ar (
            id TEXT,
            reaction TEXT
        )
    ''')

@Client.on_message(filters.command("ar", prefixes=prefix) & filters.me)
async def ar_actions(client, message):
    try:
        command = message.command[1]
    except IndexError:
        await message.edit(f"Помощь по командам - {prefix}help autoreactions")
        return
    if command == "add":
        try:
            reaction = message.command[2]
        except IndexError:
            await message.edit(f"Помощь по командам - {prefix}help autoreactions")
            return
        if reaction not in ['👍', '👎', '❤️', '🔥', '🥰', '👏', '😁', '🤔', '🤯', '😱', '😡', '😢', '😭', '🎉', '🤩', '🤮', '💩', '🙏', '👌',
                         '🕊', '🤡', '🥱', '🥴', '😍', '🐳', '❤️‍🔥', '🌚', '🌭', '💯', '🤣', '⚡️', '🍌', '🏆', '💔', '🤨', '😐', '🍓',
                         '🍾', '💋', '🖕', '😈', '😴', '😭', '🤓', '👻', '👨‍💻', '👀', '🎃', '🙈', '😇', '😨', '🤝', '✍', '🤗', '🫡',
                         '🎅', '🎄', '☃️', '💅', '🤪', '🗿', '🆒', '💘', '🙉', '😎', '👾', '🤷‍♀', '🤷', '🤷‍♂', '😡']:
            await message.edit("Такой реакции не существует в телеграме!")
            return
        if message.reply_to_message:
            c.execute("INSERT INTO ar (id, reaction) values (?, ?)", (message.reply_to_message.from_user.id, reaction))
            await message.edit("Успешно добавлен в базу автореакций!")
            conn.commit()
            return
        await message.edit("Эта команда должна быть использованная в ответ на сообщение")
        return
    elif command == "remove":
        if message.reply_to_message:
            c.execute("SELECT id FROM ar WHERE id=?", (message.reply_to_message.from_user.id,))
            row = c.fetchone()
            if row:
                c.execute("DELETE FROM ar WHERE id=?", (message.reply_to_message.from_user.id,))
                conn.commit()
                await message.edit("Успешно удалён из базы автореакций!")
                return
            await message.edit("Такого пользователя нет в базе")
            return
        await message.edit("Эта команда должна быть использованная в ответ на сообщение")
        return
    else:
        await message.edit(f"Помощь по командам - {prefix}help autoreactions")
        return

@Client.on_message(~filters.me)
async def auto_reaction(client, message):
    try:
        c.execute("SELECT reaction FROM ar WHERE id = ?", (message.from_user.id,))
        row = c.fetchone()
    except:
        return 
    if not row:
        return
    await asyncio.sleep(random.randint(1, 15))
    await client.send_reaction(message.chat.id, message.id, row[0])

add_module("autoreactions", __file__)
add_command("autoreactions", f"{prefix}ar add [реакция]", "Устанавливает автореакцию на определённого пользователя. Используется в ответ на сообщение")
add_command("autoreactions", f"{prefix}ar remove", "Удаляет пользователя из базы автореакций. Используется в ответ на сообщение")