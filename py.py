# ШАБЛОН ВЗЯТ ИЗ FoxUserBot
import html
import sys
from pyrogram import Client, filters
from io import StringIO
from helps.modules import add_module, add_command
from helps.scripts import neko
import re
import asyncio

from helps.get_prefix import get_prefix
prefix = get_prefix()


@Client.on_message(filters.command("py", prefixes=prefix) & filters.me)
async def user_exec(client, message):
    reply = message.reply_to_message
    code = ""
    try:
        code = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        try:
            code = message.text.split(" \n", maxsplit=1)[1]
        except IndexError:
            pass

    result = sys.stdout = StringIO()
    try:
        await message.edit("🔃 Выполняю...")
        if "await" in code:
            to_exec = '\n'.join('    ' + line for line in code.split('\n'))

            exec(f'''
async def __exec(client, message):
{to_exec}

loop = asyncio.get_event_loop()
loop.create_task(__exec(client, message))
            '''.replace("print", "await message.reply"))
        else:
            exec(code)

        result1 = result.getvalue()
        await message.edit(f"""
<b>Код:</b>
<pre language='python'>
<code>{code}</code>
</pre>

<b>Результат:</b>
<pre language='python'>
{result1}
</pre>
"""
        )
    except:
        await message.edit(f"""
<b>Code:</b>
<pre language='python'>
<code>{code}</code>
</pre>

<b>Result</b>:
<pre language='python'>
{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}
</pre>
        """
                           )

add_module("py", __file__)
add_command("py", f"{prefix}py [код]", "выполняет код python")