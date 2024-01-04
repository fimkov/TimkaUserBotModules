from pyrogram import Client, filters
from helps.modules import add_module, add_command
from helps.scripts import get_keys, set_key
from plugins.autoreactions import auto_reaction

from helps.get_prefix import get_prefix
prefix = get_prefix()

@Client.on_message(filters.command("aws", prefixes=prefix) & filters.me)
async def aws(client, message):
    try:
        command = message.command[1]
    except IndexError:
        info = await get_keys(['aws_text', 'aws_status'])
        await message.edit(f"На данный момент у aws такие настройки:\n\nСтатус {info[1]}\nТекст: {info[0]}")
        return
    if command == 'on':
        await set_key('aws_status', 'on')
        await message.edit('autoanswer включен')
    elif command == 'off':
        await set_key('aws_status', 'off')
        await message.edit('autoanswer выключен')
    elif command == 'set':
        try:
            text = " ".join(message.command[2:])
        except IndexError:
            await message.edit('После аргумента set должен быть текст!')
            return
        await set_key('aws_text', text)
        await message.edit("Текст успешно установлен!")

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


add_module('autoanswer', __file__)
add_command('autoanswer', f'{prefix}aws on', 'включить автоответчик')
add_command('autoanswer', f'{prefix}aws off', 'выключить автоответчик')
add_command('autoanswer', f'{prefix}aws set [текст]', 'установить текст для отправки')