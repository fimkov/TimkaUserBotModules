# PORTED FROM DragonUserBot
import pip
pip.main(['install', 'pillow', '-U'])
from typing import LiteralString
from pyrogram import Client, filters, types, errors
from helps.modules import add_module, add_command
from helps.scripts import get_lang
from helps.get_prefix import get_prefix
import requests, traceback, base64
from io import BytesIO
from PIL import Image
from pyrogram.types.messages_and_media.message import Str

lang = get_lang()
prefix = get_prefix()


def resize_image(
        input_img, output=None, img_type="PNG", size: int = 512, size2: int = None
):
    if output is None:
        output = BytesIO()
        output.name = f"sticker.{img_type.lower()}"

    with Image.open(input_img) as img:
        if size2 is not None:
            size = (size, size2)
        elif img.width == img.height:
            size = (size, size)
        elif img.width < img.height:
            size = (max(size * img.width // img.height, 1), size)
        else:
            size = (size, max(size * img.height // img.width, 1))

        img.resize(size).save(output, img_type)

    return output


def format_exc(e: Exception, suffix="") -> str:
    traceback.print_exc()
    if isinstance(e, errors.RPCError):
        return (
            f"<b>Telegram API error!</b>\n"
            f"<code>[{e.CODE} {e.ID or e.NAME}] — {e.MESSAGE.format(value=e.value)}</code>\n\n<b>{suffix}</b>"
        )
    return (
        f"<b>Error!</b>\n"
        f"<code>{e.__class__.__name__}: {e}</code>\n\n<b>{suffix}</b>"
    )


class Texts:
    @staticmethod
    def get_texts():
        return \
    {
        "generating": {
            "ru": f"<b>Генерация...</b>",
            "en": f"<b>Generating...</b>"
        },
        "sending": {
            "ru": "<b>Отправка...</b>",
            "en": "<b>Sending...</b>"
        },
        "error2": {
            "ru": "<b>Текст фейковой цитаты пуст</b>",
            "en": "<b>Fake quote text is empty</b>"
        }
    }


@Client.on_message(filters.command(["q", "quote"], prefix) & filters.me)
async def quote_cmd(client: Client, message: types.Message):
    text_versions = Texts.get_texts()
    if not message.reply_to_message:
        return
    if len(message.command) > 1 and message.command[1].isdigit():
        count = int(message.command[1])
        if count < 1:
            count = 1
        elif count > 15:
            count = 15
    else:
        count = 1

    is_png = "!png" in message.command or "!file" in message.command
    send_for_me = "!me" in message.command or "!ls" in message.command
    no_reply = "!noreply" in message.command or "!nr" in message.command

    messages = []

    async for msg in client.get_chat_history(
            message.chat.id,
            offset_id=message.reply_to_message.id + count,
            limit=count,
    ):
        if msg.empty:
            continue
        if msg.id >= message.id:
            break
        if no_reply:
            msg.reply_to_message = None

        messages.append(msg)

        if len(messages) >= count:
            break

    messages.reverse()

    if send_for_me:
        await message.delete()
        message = await client.send_message("me", text_versions["generating"][lang])
    else:
        await message.edit(text_versions["generating"][lang])

    url = "https://quotes.fl1yd.su/generate"
    params = {
        "messages": [
            await render_message(client, msg)
            for msg in messages
            if not msg.empty
        ],
        "quote_color": "#162330",
        "text_color": "#fff",
    }

    response = requests.post(url, json=params)
    if not response.ok:
        if lang == "ru":
            return await message.edit("<b>Ошибка quotes API!</b>\n" f"<code>{response.text}</code>")
        else:
            return await message.edit("<b>Quotes API error!</b>\n" f"<code>{response.text}</code>")

    resized = resize_image(
        BytesIO(response.content), img_type="PNG" if is_png else "WEBP"
    )
    await message.edit(text_versions["sending"][lang])

    try:
        func = client.send_document if is_png else client.send_sticker
        chat_id = "me" if send_for_me else message.chat.id
        await func(chat_id, resized)
    except errors.RPCError as e:
        await message.edit(format_exc(e))
    else:
        await message.delete()


@Client.on_message(filters.command(["fq", "fakequote"], prefix) & filters.me)
async def fake_quote_cmd(client: Client, message: types.Message):
    text_versions = Texts.get_texts()
    if not message.reply_to_message:
        return
    is_png = "!png" in message.command or "!file" in message.command
    send_for_me = "!me" in message.command or "!ls" in message.command
    no_reply = "!noreply" in message.command or "!nr" in message.command

    fake_quote_text = " ".join(
        [
            arg
            for arg in message.command[1:]
            if arg not in ["!png", "!file", "!me", "!ls", "!noreply", "!nr"]
        ]
    )

    if not fake_quote_text:
        return await message.edit(text_versions["error2"][lang])

    q_message = await client.get_messages(
        message.chat.id, message.reply_to_message.id
    )
    q_message.text = fake_quote_text
    q_message.entities = None
    if no_reply:
        q_message.reply_to_message = None

    if send_for_me:
        await message.delete()
        message = await client.send_message("me", text_versions["generating"][lang])
    else:
        await message.edit(text_versions["generating"][lang])

    url = "https://quotes.fl1yd.su/generate"
    params = {
        "messages": [await render_message(client, q_message)],
        "quote_color": "#162330",
        "text_color": "#fff",
    }

    response = requests.post(url, json=params)
    if not response.ok:
        text_versions = Texts.get_texts(response)
        return await message.edit(text_versions["error1"][lang])

    resized = resize_image(
        BytesIO(response.content), img_type="PNG" if is_png else "WEBP"
    )
    await message.edit(text_versions["sending"][lang])

    try:
        func = client.send_document if is_png else client.send_sticker
        chat_id = "me" if send_for_me else message.chat.id
        await func(chat_id, resized)
    except errors.RPCError as e:  # no rights to send stickers, etc
        await message.edit(format_exc(e))
    else:
        await message.delete()


files_cache = {}


async def render_message(app: Client, message: types.Message) -> dict:
    async def get_file(file_id) -> str:
        if file_id in files_cache:
            return files_cache[file_id]

        content = await app.download_media(file_id, in_memory=True)
        data = base64.b64encode(bytes(content.getbuffer())).decode()
        files_cache[file_id] = data
        return data

    # text
    if message.photo:
        text = message.caption if message.caption else ""
    elif message.poll:
        text = get_poll_text(message.poll)
    elif message.sticker:
        text = ""
    else:
        text = get_reply_text(message)

    # media
    if message.photo:
        media = await get_file(message.photo.file_id)
    elif message.sticker:
        media = await get_file(message.sticker.file_id)
    else:
        media = ""

    # entities
    entities = []
    if message.entities:
        for entity in message.entities:
            entities.append(
                {
                    "offset": entity.offset,
                    "length": entity.length,
                    "type": str(entity.type).split(".")[-1].lower(),
                }
            )

    def move_forwards(msg: types.Message):
        if msg.forward_from:
            msg.from_user = msg.forward_from
        if msg.forward_sender_name:
            msg.from_user.id = 0
            msg.from_user.first_name = msg.forward_sender_name
            msg.from_user.last_name = ""
        if msg.forward_from_chat:
            msg.sender_chat = msg.forward_from_chat
            msg.from_user.id = 0
        if msg.forward_signature:
            msg.author_signature = msg.forward_signature

    move_forwards(message)

    # author
    author = {}
    if message.from_user and message.from_user.id != 0:
        from_user = message.from_user

        author["id"] = from_user.id
        author["name"] = get_full_name(from_user)
        if message.author_signature:
            author["rank"] = message.author_signature
        elif message.chat.type != "supergroup" or message.forward_date:
            author["rank"] = ""
        else:
            try:
                member = await message.chat.get_member(from_user.id)
            except errors.UserNotParticipant:
                author["rank"] = ""
            else:
                author["rank"] = getattr(member, "title", "") or (
                    "owner"
                    if member.status == "creator"
                    else "admin"
                    if member.status == "administrator"
                    else ""
                )

        if from_user.photo:
            author["avatar"] = await get_file(from_user.photo.big_file_id)
        elif not from_user.photo and from_user.username:
            # may be user blocked us, we will try to get avatar via t.me
            t_me_page = requests.get(f"https://t.me/{from_user.username}").text
            sub = '<meta property="og:image" content='
            index = t_me_page.find(sub)
            if index != -1:
                link = t_me_page[index + 35:].split('"')
                if (
                        len(link) > 0
                        and link[0]
                        and link[0] != "https://telegram.org/img/t_logo.png"
                ):
                    # found valid link
                    avatar = requests.get(link[0]).content
                    author["avatar"] = base64.b64encode(avatar).decode()
                else:
                    author["avatar"] = ""
            else:
                author["avatar"] = ""
        else:
            author["avatar"] = ""
    elif message.from_user and message.from_user.id == 0:
        author["id"] = 0
        author["name"] = message.from_user.first_name
        author["rank"] = ""
    else:
        author["id"] = message.sender_chat.id
        author["name"] = message.sender_chat.title
        author["rank"] = (
            "channel" if message.sender_chat.type == "channel" else ""
        )

        if message.sender_chat.photo:
            author["avatar"] = await get_file(
                message.sender_chat.photo.big_file_id
            )
        else:
            author["avatar"] = ""
    author["via_bot"] = message.via_bot.username if message.via_bot else ""

    # reply
    reply = {}
    reply_msg = message.reply_to_message
    if reply_msg and not reply_msg.empty:
        move_forwards(reply_msg)

        if reply_msg.from_user:
            reply["id"] = reply_msg.from_user.id
            reply["name"] = get_full_name(reply_msg.from_user)
        else:
            reply["id"] = reply_msg.sender_chat.id
            reply["name"] = reply_msg.sender_chat.title

        reply["text"] = get_reply_text(reply_msg)

    return {
        "text": text,
        "media": media,
        "entities": entities,
        "author": author,
        "reply": reply,
    }


def get_audio_text(audio: types.Audio) -> str:
    if audio.title and audio.performer:
        return f" ({audio.title} — {audio.performer})"
    elif audio.title:
        return f" ({audio.title})"
    elif audio.performer:
        return f" ({audio.performer})"
    else:
        return ""


def get_reply_text(reply: types.Message) -> LiteralString | str | Str | None:
    return (
        "📷 Photo" + ("\n" + reply.caption if reply.caption else "")
        if reply.photo
        else get_reply_poll_text(reply.poll)
        if reply.poll
        else "📍 Location"
        if reply.location or reply.venue
        else "👤 Contact"
        if reply.contact
        else "🖼 GIF"
        if reply.animation
        else "🎧 Music" + get_audio_text(reply.audio)
        if reply.audio
        else "📹 Video"
        if reply.video
        else "📹 Videomessage"
        if reply.video_note
        else "🎵 Voice"
        if reply.voice
        else (reply.sticker.emoji + " " if reply.sticker.emoji else "")
             + "Sticker"
        if reply.sticker
        else "💾 File " + reply.document.file_name
        if reply.document
        else "🎮 Game"
        if reply.game
        else "🎮 set new record"
        if reply.game_high_score
        else f"{reply.dice.emoji} - {reply.dice.value}"
        if reply.dice
        else (
            "👤 joined the group"
            if reply.new_chat_members[0].id == reply.from_user.id
            else "👤 invited %s to the group"
                 % (get_full_name(reply.new_chat_members[0]))
        )
        if reply.new_chat_members
        else (
            "👤 left the group"
            if reply.left_chat_member.id == reply.from_user.id
            else "👤 removed %s" % (get_full_name(reply.left_chat_member))
        )
        if reply.left_chat_member
        else f"✏ changed group name to {reply.new_chat_title}"
        if reply.new_chat_title
        else "🖼 changed group photo"
        if reply.new_chat_photo
        else "🖼 removed group photo"
        if reply.delete_chat_photo
        else "📍 pinned message"
        if reply.pinned_message
        else "🎤 started a new video chat"
        if reply.video_chat_started
        else "🎤 ended the video chat"
        if reply.video_chat_ended
        else "🎤 invited participants to the video chat"
        if reply.video_chat_members_invited
        else "👥 created the group"
        if reply.group_chat_created or reply.supergroup_chat_created
        else "👥 created the channel"
        if reply.channel_chat_created
        else reply.text or "unsupported message"
    )


def get_poll_text(poll: types.Poll) -> str:
    text = get_reply_poll_text(poll) + "\n"

    text += poll.question + "\n"
    for option in poll.options:
        text += f"- {option.text}"
        if option.voter_count > 0:
            text += f" ({option.voter_count} voted)"
        text += "\n"

    text += f"Total: {poll.total_voter_count} voted"

    return text


def get_reply_poll_text(poll: types.Poll) -> str:
    if poll.is_anonymous:
        text = (
            "📊 Anonymous poll" if poll.type == "regular" else "📊 Anonymous quiz"
        )
    else:
        text = "📊 Poll" if poll.type == "regular" else "📊 Quiz"
    if poll.is_closed:
        text += " (closed)"

    return text


def get_full_name(user: types.User) -> str:
    name = user.first_name
    if user.last_name:
        name += " " + user.last_name
    return name


if lang == "ru":
    add_module("quotes", __file__)
    add_command("quotes", f"{prefix}q [ответ] [количество 1-15] [!png] [!me] [!noreply]", "Генирирует цитату")
    add_command("quotes", f"{prefix}fq [ответ] [!png] [!me] [!noreply] [текст]", "Генирирует фейковую цитату")
else:
    add_module("quotes", __file__)
    add_command("quotes", f"{prefix}q [reply] [count 1-15] [!png] [!me] [!noreply]", "Generate a quote")
    add_command("quotes", f"{prefix}fq [reply] [!png] [!me] [!noreply] [text]", "Generate a fake quote")
