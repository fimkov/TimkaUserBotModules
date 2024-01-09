from pyrogram import Client, filters
from helps.modules import add_module, add_command
from helps.scripts import get_keys, set_key
import asyncio
import random
from main import c, conn
from helps.get_prefix import get_prefix
from helps.scripts import get_lang

lang = get_lang()
prefix = get_prefix()

c.execute('''
        CREATE TABLE IF NOT EXISTS ar (
            id TEXT,
            reaction TEXT
        )
    ''')


class Texts:
    @staticmethod
    def get_texts():
        return {
            "error": {
                "ru": f"Помощь по командам - {prefix}help autoreactions",
                "en": f"Help by commands - {prefix}help autoreactions"
            },
            "successfully add": {
                "ru": "Успешно добавлен в базу автореакций!",
                "en": "Successfully added to the autoreactions database!"
            },
            "successfully removed": {
                "ru": "Успешно удалён из базы автореакций!",
                "en": "Successfully deleted from the database of autoreactions!"
            },
            "not found": {
                "ru": "Такого пользователя нет в базе",
                "en": "There is no such user in the database"
            }
        }


@Client.on_message(filters.command("ar", prefixes=prefix) & filters.me)
async def ar_actions(_, message):
    text_versions = Texts.get_texts()
    try:
        command = message.command[1]
    except IndexError:
        await message.edit(text_versions['error'][lang])
        return
    if command == "add":
        try:
            reaction = message.command[2]
        except IndexError:
            await message.edit(text_versions['error'][lang])
            return
        if reaction not in ['👍', '👎', '❤️', '🔥', '🥰', '👏', '😁', '🤔', '🤯', '😱', '😡', '😢', '😭', '🎉', '🤩', '🤮', '💩', '🙏',
                            '👌',
                            '🕊', '🤡', '🥱', '🥴', '😍', '🐳', '❤️‍🔥', '🌚', '🌭', '💯', '🤣', '⚡️', '🍌', '🏆', '💔', '🤨', '😐',
                            '🍓',
                            '🍾', '💋', '🖕', '😈', '😴', '😭', '🤓', '👻', '👨‍💻', '👀', '🎃', '🙈', '😇', '😨', '🤝', '✍', '🤗', '🫡',
                            '🎅', '🎄', '☃️', '💅', '🤪', '🗿', '🆒', '💘', '🙉', '😎', '👾', '🤷‍♀', '🤷', '🤷‍♂', '😡']:
            await message.edit(text_versions['error'][lang])
            return
        if message.reply_to_message:
            c.execute("INSERT INTO ar (id, reaction) values (?, ?)", (message.reply_to_message.from_user.id, reaction))
            await message.edit(text_versions['successfully add'][lang])
            conn.commit()
            return
        await message.edit(text_versions['error'][lang])
        return
    elif command == "remove":
        if message.reply_to_message:
            c.execute("SELECT id FROM ar WHERE id=?", (message.reply_to_message.from_user.id,))
            row = c.fetchone()
            if row:
                c.execute("DELETE FROM ar WHERE id=?", (message.reply_to_message.from_user.id,))
                conn.commit()
                await message.edit(text_versions['successfully removed'][lang])
                return
            await message.edit(text_versions['not found'][lang])
            return
        await message.edit(text_versions['error'][lang])
        return
    else:
        await message.edit(text_versions['error'][lang])
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

if lang == "ru":
    add_module("autoreactions", __file__)
    add_command("autoreactions", f"{prefix}ar add [реакция]",
            "Устанавливает автореакцию на определённого пользователя. Используется в ответ на сообщение")
    add_command("autoreactions", f"{prefix}ar remove",
            "Удаляет пользователя из базы автореакций. Используется в ответ на сообщение")
else:
    add_module("autoreactions", __file__)
    add_command("autoreactions", f"{prefix}ar add [reaction]",
                "Sets an autoreaction for a specific user. Used in response to a message.")
    add_command("autoreactions", f"{prefix}ar remove",
                "Removes a user from the autoreactions database. Used in response to a message.")
