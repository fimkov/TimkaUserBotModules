# ported from FoxUserBot
import datetime
from pyrogram import Client, filters, types
from helps.modules import add_module, add_command

from helps.get_prefix import get_prefix
prefix = get_prefix()

afk_info = {
    "start": datetime.datetime.now(),
    "is_afk": False,
    "reason": "",
}

is_afk = filters.create(lambda _, __, ___: afk_info["is_afk"])


@Client.on_message(is_afk & ~filters.me & ((filters.private & ~filters.bot) | (filters.mentioned & filters.group)))
async def afk_handler(_, message: types.Message):
    end = datetime.datetime.now().replace(microsecond=0)
    afk_time = end - afk_info["start"]
    await message.reply_text(
        f"❕ Этот юзер в <b>АФК</b>.\n💬 Причина:</b> <i>{afk_info['reason']}</i>\n<b>⏳ Прошло с ухода в афк:</b> {afk_time}"
    )


@Client.on_message(filters.command("afk", prefix) & filters.me)
async def afk(_, message):
    if len(message.text.split()) >= 2:
        reason = message.text.split(" ", maxsplit=1)[1]
    else:
        reason = "Не указана"

    afk_info["start"] = datetime.datetime.now().replace(microsecond=0)
    afk_info["is_afk"] = True
    afk_info["reason"] = reason

    await message.edit(f"❕ Я ухожу в <b>АФК</b>.\n<b>💬 Причина:</b> <i>{reason}</i>.")


@Client.on_message(filters.command("unafk", prefix) & filters.me)
async def unafk(_, message):
    if afk_info["is_afk"]:
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = end - afk_info["start"]
        await message.edit(f"<b>❕ Я больше не в <b>АФК</b>.\n" f"⏳ Я пробыл в <b>АФК:</b> {afk_time}")
        afk_info["is_afk"] = False
    else:
        await message.edit("<b>❌ Вы не были в афк</b>")

add_module("afk", __file__)
add_command("afk", f"{prefix}afk [причина]", "войти в афк режим")
add_command("unafk", f"{prefix}unafk", "выйти из афк режима")