from pyrogram import Client, filters, enums
from helps.modules import add_module, add_command
from helps.scripts import restart
from helps.get_prefix import get_prefix
from helps.scripts import get_lang

lang = get_lang()
prefix = get_prefix()


class Texts:
    @staticmethod
    def get_texts():
        return {
            "help": {
                "ru": f"Помощь по команде: {prefix}help tagall",
                "en": f"Command help: {prefix}help tagall"
            }
        }


@Client.on_message(filters.command("tagall", prefixes=prefix) & filters.me)
async def tagall(client, message):
    text_versions = Texts.get_texts()
    try:
        arg = message.text.replace(f"{prefix}tag ", "")
    except:
        return await message.edit(text_versions["help"][lang])

    tags = ""
    count = 0
    count_members = await client.get_chat_members_count(chat_id=message.chat.id)
    if count_members <= 5:
        async for member in client.get_chat_members(message.chat.id):
            tags = tags + " " + member.user.mention("<spoiler>.</spoiler>")
            await message.edit(f"{arg} | {tags}")
    else:
        async for member in client.get_chat_members(message.chat.id):
            if count == 5:
                await message.reply(f"{arg} | {tags}")
                count = 0
                tags = ""
            else:
                tags = tags + " " + member.user.mention("<spoiler>.</spoiler>")
                count = + 1

if lang == "ru":
    add_module("tagall", __file__)
    add_command("tagall", f"{prefix}tagall [текст]", "Отметит всех участников чата")
else:
    add_module("tagall", __file__)
    add_command("tagall", f"{prefix}tagall [text]", "Mention all chat members")