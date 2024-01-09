from pyrogram import Client, filters
from helps.modules import add_module, add_command
from helps.scripts import get_keys, set_key
from plugins.autoreactions import auto_reaction
from helps.get_prefix import get_prefix
from helps.scripts import get_lang

lang = get_lang()
prefix = get_prefix()


class Texts:
    @staticmethod
    def get_texts(info):
        return {
            "aws_info": {
                "ru": f"На данный момент у aws такие настройки:\n\nСтатус {info[1]}\nТекст: {info[0]}",
                "en": f"At the moment, aws has these settings:\n\n Status {info[1]}\Text: {info[0]}"
            },
            "aws_status": {
                "on": {
                    "ru": "autoanswer включен",
                    "en": "autoanswer on"
                },
                "off": {
                    "ru": "autoanswer выключен",
                    "en": "autoanswer off"
                }
            },
            "error": {
                "ru": "После аргумента set должен быть текст!",
                "en": "There should be text after the set argument!"
            },
            "successfully": {
                "ru": "Текст успешно установлен!",
                "en": "Text successfully installed!"
            }
        }


@Client.on_message(filters.command("aws", prefixes=prefix) & filters.me)
async def aws(client, message):
    info = await get_keys(['aws_text', 'aws_status'])
    text_versions = Texts.get_texts(info)

    try:
        command = message.command[1]
    except IndexError:
        await message.edit(text_versions['aws_info'][lang])
        return

    if command == 'on':
        await set_key('aws_status', 'on')
        await message.edit(text_versions['aws_status']['on'][lang])
    elif command == 'off':
        await set_key('aws_status', 'off')
        await message.edit(text_versions['aws_status']['off'][lang])
    elif command == 'set':
        try:
            text = " ".join(message.command[2:])
        except IndexError:
            await message.edit(text_versions['error'][lang])
            return
        await set_key('aws_text', text)
        await message.edit(text_versions['successfully'][lang])


@Client.on_message(filters.private & ~filters.me & ~filters.bot)
async def autoasw(client, message):
    messages = await client.get_chat_history_count(chat_id=message.chat.id)
    if messages == 2:
        text = await get_keys(['aws_text', 'aws_status'])

        if text[1] == 'off':
            await auto_reaction(client, message)
            return
        if text[0]:
            await message.reply(text[0])
    else:
        pass
    await auto_reaction(client, message)

if lang == "ru":
    add_module('autoanswer', __file__)
    add_command('autoanswer', f'{prefix}aws on', 'включить автоответчик')
    add_command('autoanswer', f'{prefix}aws off', 'выключить автоответчик')
    add_command('autoanswer', f'{prefix}aws set [текст]', 'установить текст для отправки')
else:
    add_module('autoanswer', __file__)
    add_command('autoanswer', f'{prefix}aws on', 'turn on the answering machine')
    add_command('autoanswer', f'{prefix}aws off', 'turn off the answering machine')
    add_command('autoanswer', f'{prefix}aws set [text]', 'set the text to send')
