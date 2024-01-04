import datetime
from pyrogram import Client, filters
from helps.modules import add_module, add_command

from helps.get_prefix import get_prefix
prefix = get_prefix()

@Client.on_message(filters.command("uptime", prefixes=prefix))
async def uptime_get(client, message):
    await message.edit(
        f"<b>uptime TimkaUserBot:</b>:\n{datetime.datetime.now().replace(microsecond=0) - start}"
    )

start = datetime.datetime.now().replace(microsecond=0)
add_module("uptime", __file__)
add_command("uptime", f"{prefix}uptime", "показывает аптайм юзербота")