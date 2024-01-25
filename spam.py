import asyncio
from pyrogram import Client, filters
from helps.modules import add_module, add_command
from helps.get_prefix import get_prefix
from helps.scripts import get_lang

lang = get_lang()
prefix = get_prefix()

spam = False


class Texts:
    @staticmethod
    def get_texts():
        return {
            "errors": {
                "already": {
                    "ru": "Спам уже запущен",
                    "en": "Spam has already been launched"
                },
                "not": {
                    "ru": "Спам не запущен!",
                    "en": "Spam is not running!"
                },
                "help": {
                    "ru": f"Посмотрите использование команды с помощью {prefix}help spam",
                    "en": f"See the use of the command using {prefix}help spam"
                }
            },
            "start": {
                "ru": f"Спам начат! Чтобы его остановить введите команду {prefix}stop_spam",
                "en": f"Spam has started! To stop it, enter the command {prefix}stop_spam"
            },
            "stop": {
                "ru": "Спам остановлен!",
                "en": "Spam has been stopped!"
            }
        }


@Client.on_message(filters.command("spam", prefixes=prefix) & filters.me)
async def spam_func(client, message):
    text_versions = Texts.get_texts()

    global spam

    if spam == True:
        await message.edit(text_versions['errors']['already'][lang])

    try:
        count = message.command[1]
        time = float(message.command[2])
        text = " ".join(message.command[3:])
    except IndexError:
        await message.edit(text_versions['errors']['helps'][lang])
        return

    spam = True
    await message.edit(text_versions['start'][lang])

    for i in range(int(count)):

        if not spam:
            break
        await client.send_message(chat_id=message.chat.id, text=text)
        await asyncio.sleep(time)

    spam = False


@Client.on_message(filters.command("stop_spam", prefixes=prefix) & filters.me)
async def stop_spam(client, message):
    global spam
    text_versions = Texts.get_texts()

    if not spam:
        await message.edit(text_versions['errors']['not'][lang])
        return

    spam = False

    await message.edit(text_versions['stop'][lang])

if lang == "ru":
    add_module("spam", __file__)
    add_command("spam", f"{prefix}spam [кол-во сообщений] [задержка] [текс]", "запустить спам")
    add_command("spam", f"{prefix}stop_spam", "остановить спам")
else:
    add_module("spam", __file__)
    add_command("spam", f"{prefix}spam [number of messages] [delay] [tex]", "start spam")
    add_command("spam", f"{prefix}stop_spam", "stop spam")
