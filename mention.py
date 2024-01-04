from pyrogram import Client, filters
from helps.modules import add_module, add_command

from helps.get_prefix import get_prefix
prefix = get_prefix()

@Client.on_message(filters.command("mention", prefix) & filters.me)
async def mention(client, message):
    try:
        id = message.text.split(maxsplit=1)[1]
        text = message.text.split(maxsplit=1)[2]
    except IndexError:
        await message.edit("Вы не правильно используете команду! Помощь - !help mention")
        return
    await message.edit(f"<a href='{id}'>{text}</a>")

add_module("mention", __file__)
add_command("mention", f"{prefix}mention [айди пользователя] [текст пометки]", "делает упоминание пользователя имея только его айди")