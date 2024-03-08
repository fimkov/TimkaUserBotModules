from pyrogram import Client, filters
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
                "ru": f"Помощь по команде: {prefix}help triggers",
                "en": f"Command help: {prefix}help triggers"
            },
            "successfully": {
                "ru": "Команда успешно создана!",
                "en": "The command has been successfully created!"
            },
            "reload": {
                "ru": "<b>Перезагружаю юзербота...</b>",
                "en": "<b>Rebooting the userbot...</b>"
            }
        }


@Client.on_message(filters.command("trigger", prefix) & filters.me)
async def anim_add(client, message):
    text_versions = Texts.get_texts()
    try:
        name = message.command[1]
    except IndexError:
        await message.edit(text_versions["help"][lang])
        return
    code = f"""from pyrogram import Client, filters
from helps.modules import add_module, add_command
import asyncio
from helps.get_prefix import get_prefix
from helps.scripts import get_lang

lang = get_lang()
prefix = get_prefix()

@Client.on_message(filters.command("{name}", prefix) & filters.me)
async def {name}(client, message):"""

    aims = message.text.splitlines()
    i = 0
    o = 0

    for a in aims:
        if i == 0:
            pass
        else:
            b = a.split()
            if b[0] == "edit":
                if o == 0:
                    code = code + f"\n    await message.edit('{a.replace(b[0] + ' ', '')}')"
                else:
                    code = code + f"\n    await pensil.edit('{a.replace(b[0] + ' ', '')}')"
            elif b[0] == "send":
                o = 1
                code = code + f"\n    pensil = await message.reply('{a.replace(b[0] + ' ', '')}')"
            elif b[0] == "sleep":
                code = code + f"\n    await asyncio.sleep({a.replace(b[0] + ' ', '')})"
            elif b[0] == "remove":
                if o == 0:
                    code = code + f"\n    await message.delete()"
                else:
                    code = code + f"\n    await pensil.delete()"
            else:
                code = code + f"\n    await message.edit('{a}')"

        i = i + 1

    code = code + "\n\nif lang == 'ru':"
    code = code + f"\n    add_module('{name}', __file__)"
    code = code + f"\n    add_command('{name}', '{prefix}{name}', 'кастомная анимация')"
    code = code + "\nelse:"
    code = code + f"\n    add_module('{name}', __file__)"
    code = code + f"\n    add_command('{name}', '{prefix}{name}', 'custom animation')"

    f = open(f"plugins/{name}.py", "w", encoding='utf-8')
    f.write(code)
    f.close()

    await message.edit(text_versions['successfully'][lang])
    await message.reply(text_versions['reload'][lang])
    await restart(message=message)


if lang == "ru":
    add_module("triggers", __file__)
    add_command("triggers",
                f"{prefix}trigger [имя команды] и дальше на каждой новой строке действие и аргумент. Все действия: https://telegra.ph/Using-the-triggers-module-03-08",
                "создаёт кастомную анимацию")
else:
    add_module("triggers", __file__)
    add_command("triggers",
                f"{prefix}trigger [command name] and then on each new line an action and an argument. All actions: https://telegra.ph/Using-the-triggers-module-03-08",
                "creates custom animation")
