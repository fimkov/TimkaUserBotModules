from pyrogram import Client, filters
from helps.modules import add_module, add_command
from helps.scripts import restart

from helps.get_prefix import get_prefix
prefix = get_prefix()

@Client.on_message(filters.command("trigger", prefix) & filters.me)
async def anim_add(client, message):
    try:
        name = message.command[1]
        sleep = message.command[2]
    except IndexError:
        await message.edit(f"Помощь по команде: {prefix}help triggers")
        return
    code = f"""from pyrogram import Client, filters
from helps.modules import add_module, add_command
import asyncio

from helps.get_prefix import get_prefix
prefix = get_prefix()

@Client.on_message(filters.command("{name}", prefix) & filters.me)
async def {name}(client, message):"""

    aims = message.text.splitlines()
    i = 0

    for a in aims:
        if i == 0:
            pass
        else:
            code = code + f"\n    await message.edit('{a}')\n    await asyncio.sleep({sleep})"

        i = i + 1

    code = code + f"\n\nadd_module('{name}')"
    code = code + f"\nadd_command('{name}', '{prefix}{name}', 'кастомная анимация')"

    f = open(f"plugins/{name}.py", "w", encoding='utf-8')
    f.write(code)
    f.close()

    await message.edit("Команда успешно создана!")
    await message.reply("<b>Перезагружаю юзербота...</b>")
    await restart(message=message.chat.id)

add_module("triggers", __file__)
add_command("triggers", f"{prefix}trigger [имя команды] [задержка между изменениями] и дальше на каждой новой строке текст для изменения", "создаёт кастомную анимацию")