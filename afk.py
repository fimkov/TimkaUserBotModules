# ported from FoxUserBot
import datetime
from pyrogram import Client, filters, types
from helps.modules import add_module, add_command
from helps.get_prefix import get_prefix
from helps.scripts import get_lang

lang = get_lang()
prefix = get_prefix()

afk_info = {
    "start": datetime.datetime.now(),
    "is_afk": False,
    "reason": "",
}

is_afk = filters.create(lambda _, __, ___: afk_info["is_afk"])

class Texts:
    @staticmethod
    def get_texts():
        return {
            "afk_join": {
            "ru": f"❕ Я ухожу в <b>АФК</b>.\n<b>💬 Причина:</b> <i>{afk_info['reason']}</i>.",
            "en": f"❕ I'm going to <b>AFK</b>.\n<b>💬 Reason:</b> <i>{afk_info['reason']}</i>."
        },
            "afk_info": {
                "ru": f"❕ Этот юзер в <b>АФК</b>.\n💬 Причина:</b> <i>{afk_info['reason']}</i>\n<b>⏳ Прошло с ухода в афк:</b> {datetime.datetime.now().replace(microsecond=0) - afk_info['start']}",
                "en": f"❕ This user is in the <b>AFK</b>.\n💬 Reason:</b> <i>{afk_info['reason']}</i>\n<b>⏳ Passed since leaving afk:</b> {datetime.datetime.now().replace(microsecond=0) - afk_info['start']}"
            },
            "unafk": {
                "error": {
                    "ru": "<b>❌ Вы не были в АФК</b>",
                    "en": "<b>❌ You have not been to AFK</b>"
                },
                "info": {
                    "ru": f"<b>❕ Я больше не в <b>АФК</b>.\n" f"⏳ Я пробыл в <b>АФК:</b> {datetime.datetime.now().replace(microsecond=0) - afk_info['start']}",
                    "en": f"<b>❕ I am no longer in the <b>AFK</b>.\n" f"⏳ I stayed at <b>AFK:</b> {datetime.datetime.now().replace(microsecond=0) - afk_info['start']}"
                }
            }
        }

@Client.on_message(is_afk & ~filters.me & ((filters.private & ~filters.bot) | (filters.mentioned & filters.group)))
async def afk_handler(_, message: types.Message):
    text_versions = Texts.get_texts()

    await message.reply_text(text_versions['afk_info'][lang])


@Client.on_message(filters.command("afk", prefix) & filters.me)
async def afk(_, message):
    if len(message.text.split()) >= 2:
        reason = message.text.split(" ", maxsplit=1)[1]
    else:
        reason = "Не указана"

    afk_info["start"] = datetime.datetime.now().replace(microsecond=0)
    afk_info["is_afk"] = True
    afk_info["reason"] = reason
    text_versions = Texts.get_texts()

    await message.edit(text_versions['afk_join'][lang])


@Client.on_message(filters.command("unafk", prefix) & filters.me)
async def unafk(_, message):
    text_versions = Texts.get_texts()
    if afk_info["is_afk"]:
        await message.edit(text_versions['unafk']['info'][lang])
        afk_info["is_afk"] = False
    else:
        await message.edit(text_versions['unafk']['error'][lang])

if lang == "ru":
    add_module("afk", __file__)
    add_command("afk", f"{prefix}afk [причина]", "войти в афк режим")
    add_command("unafk", f"{prefix}unafk", "выйти из афк режима")
else:
    add_module("afk", __file__)
    add_command("afk", f"{prefix}afk [reason]", "enter afk mode")
    add_command("unafk", f"{prefix}unafk", "exit afk mode")
