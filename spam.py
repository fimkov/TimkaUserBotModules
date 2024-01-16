import asyncio
from pyrogram import Client, filters
from helps.modules import add_module, add_command

from helps.get_prefix import get_prefix
prefix = get_prefix()

spam = False

@Client.on_message(filters.command("spam", prefixes=prefix) & filters.me)
async def spam_func(client, message):
    global spam
    if spam == True:
        await message.edit("Спам уже запущен")
        return
    try:
        count = message.command[1]
        time = message.command[2]
        text = " ".join(message.command[3:])
    except IndexError:
        print(f"{count} {time} {text}")
        await message.edit(f"Посмотрите использование команды с помощью {prefix}help spam")
        return
    spam = True
    await message.edit(f"Спам начат! Чтобы его остановить введите команду {prefix}stop_spam")
    for i in range(int(count)):
        if spam == False:
            break
            return
        await client.send_message(chat_id=message.chat.id, text=text)
        await asyncio.sleep(int(time))
    spam = False

@Client.on_message(filters.command("stop_spam", prefixes=prefix) & filters.me)
async def stop_spam(client, message):
    global spam
    if spam == False:
        await message.edit("Спам не запущен!")
        return
    spam = False
    await message.edit("Спам остановлен!")

add_module("spam", __file__)
add_command("spam", f"{prefix}spam [кол-во сообщений] [задержка] [текс]", "запустить спам")
add_command("spam", f"{prefix}stop_spam", "остановить спам")
