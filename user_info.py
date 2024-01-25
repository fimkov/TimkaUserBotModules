from pyrogram import Client, filters
from helps.modules import add_module, add_command
from helps.get_prefix import get_prefix
from helps.scripts import get_lang

lang = get_lang()
prefix = get_prefix()


class Texts:
    @staticmethod
    def get_texts(log=None, info=None):
        return {
            "errors": {
                "index": {
                    "ru": "Эта команда должна использоваться либо ответом либо должен быть указан юзернейм/айди после команды",
                    "en": "This command must be used either as a response or the username/id must be specified after the command"
                },
                "log": {
                    "ru": f"Возникла ошибка! LOG:\n{log}",
                    "en": f"An error has occurred! LOG:\n{log}"
                }
            },
            "info": {
                "ru": f"""
👤 {info.mention}
<b>├  Айди:</b> <code>{info.id}</code>
<b>├  Юзернейм:</b> <code>@{info.username}</code>
<b>├  Упоминание:</b> {info.mention}
<b>├  Имя:</b> <code>{info.first_name}</code>
<b>├  Бот:</b> <code>{info.is_bot}</code>
<b>├  Контакт:</b> <code>{info.is_contact}</code>
<b>├  Взаимный контакт:</b> <code>{info.is_mutual_contact}</code>
<b>├  Удалён:</b> <code>{info.is_deleted}</code>
<b>├  Скам:</b> <code>{info.is_scam}</code>
<b>├  Премиум-подписка:</b> <code>{info.is_premium}</code>
<b>├  Статус:</b> <code>{str(info.status).replace("UserStatus.", "")}</code>
<b>└  Дата-центр:</b> <code>{info.dc_id}</code>
    """.replace("True", "да").replace("False", "нет"),
                "en": f"""
👤 {info.mention}
<b>├  ID:</b> <code>{info.id}</code>
<b>├  USERNAME:</b> <code>@{info.username}</code>
<b>├  MENTION:</b> {info.mention}
<b>├  NAME:</b> <code>{info.first_name}</code>
<b>├  IS BOT:</b> <code>{info.is_bot}</code>
<b>├  CONTACT:</b> <code>{info.is_contact}</code>
<b>├  MUTUAL CONTACT:</b> <code>{info.is_mutual_contact}</code>
<b>├  DELETED:</b> <code>{info.is_deleted}</code>
<b>├  SCAM:</b> <code>{info.is_scam}</code>
<b>├  PREMIUM-SUBSCRIPTION:</b> <code>{info.is_premium}</code>
<b>├  STATUS:</b> <code>{str(info.status).replace("UserStatus.", "")}</code>
<b>├  DC:</b> <code>{info.dc_id}</code>
    """.replace("True", "yes").replace("False", "no")
            }
        }


@Client.on_message(filters.command("user_info", prefixes=prefix) & filters.me)
async def user_info(client, message):
    if message.reply_to_message:
        id = message.reply_to_message.from_user.id
    else:
        try:
            id = message.command[1]
        except IndexError:
            text_versions = Texts.get_texts()
            await message.edit(text_versions['errors']['index'][lang])
            return
    try:
        info = await client.get_users(id)
    except Exception as e:
        text_versions = Texts.get_texts(log=e)
        await message.edit(text_versions['error']['log'][lang])
        return

    text_versions = Texts.get_texts(info=info)
    await message.edit(text_versions['info'][lang])


if lang == "ru":
    add_module("user_info", __file__)
    add_command("user_info", f"{prefix}user_info",
                "Получить информацию о пользователе. Эта команда должна использоваться либо ответом либо должен быть указан юзернейм/айди после команды")
else:
    add_module("user_info", __file__)
    add_command("user_info", f"{prefix}user_info",
                "Get information about the user. This command must be used either as a response or the username/id must be specified after the command")
