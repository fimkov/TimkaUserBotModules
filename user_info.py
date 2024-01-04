from pyrogram import Client, filters
from helps.modules import add_module, add_command

from helps.get_prefix import get_prefix
prefix = get_prefix()

@Client.on_message(filters.command("user_info", prefixes=prefix) & filters.me)
async def user_info(client, message):
    if message.reply_to_message:
        id = message.reply_to_message.from_user.id
    else:
        try:
            id = message.command[1]
        except IndexError:
            await message.edit("Эта команда должна использоваться либо ответом либо должен быть указан юзернейм/айди после команды")
            return
    try:
        info = await client.get_users(id)
    except Exception as e:
        await message.edit(f"Возникла ошибка! LOG:\n{e}")
        return
    await message.edit(f"""
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
<b>├  Дата-центр:</b> <code>{info.dc_id}</code>
    """.replace("True", "да").replace("False", "нет"))

add_module("user_info", __file__)
add_command("user_info", f"{prefix}user_info", "Получить информацию о пользователе. Эта команда должна использоваться либо ответом либо должен быть указан юзернейм/айди после команды")