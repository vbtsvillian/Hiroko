import requests
import asyncio
import arq
from PIL import Image, ImageDraw
from io import BytesIO
from Hiroko import Hiroko
from pyrogram.types import Message
from pyrogram import Client, filters




@Hiroko.on_message(filters.command('search'))
def handle_search(client :Hiroko, message):
    query = message.text.split('/search ', 1)[1]    
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    data = response.json()

    if 'extract' in data:
        result = data['extract']
    else:
        result = "Sorry, no result found."

    image = Image.new('RGB', (500, 500))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), result, fill=(255, 255, 255))

    image_file = BytesIO()
    image.save(image_file, 'PNG')
    image_file.seek(0)
    
    client.send_photo(message.chat.id, photo=image_file, caption=f"**Wikipedia search: {query}** \n\n**Result:**\n{result}")



@Hiroko.on_message(filters.command("webss"))
async def take_ss(_, message: Message):
    try:
        if len(message.command) != 2:
            return await message.reply_text(
                "Give a URL to fetch screenshot."
            )
        url = message.text.split(None, 1)[1]
        m = await message.reply_text("Taking screenshot")
        await m.edit("Uploading...")
        try:
            await message.reply_photo(
                photo=f"https://webshot.amanoteam.com/print?q={url}",
                quote=False,
            )
        except TypeError:
            return await m.edit("No such website may be you don't use .com.")
        await m.delete()
    except Exception as e:
        await message.reply_text(str(e))



async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message: Message) -> str:
    return message.text.strip().split(None, 1)[1].strip()


def isArgInt(message: Message) -> list:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]


@Hiroko.on_message(filters.command("q"))
async def quotly_func(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to quote it.")
    if not message.reply_to_message.text:
        return await message.reply_text("Replied message has no text, can't quote it.")
    m = await message.reply_text("Quoting messages")
    if len(message.command) < 2:
        messages = [message.reply_to_message]

    elif len(message.command) == 2:
        arg = isArgInt(message)
        if arg[0]:
            if arg[1] < 2 or arg[1] > 10:
                return await m.edit("Argument must be between 2-10.")

            count = arg[1]

            # Fetching 5 extra messages so that we can ignore media
            # messages and still end up with correct offset
            messages = [
                i
                for i in await client.get_messages(
                    message.chat.id,
                    range(
                        message.reply_to_message.id,
                        message.reply_to_message.id + (count + 5),
                    ),
                    replies=0,
                )
                if not i.empty and not i.media
            ]
            messages = messages[:count]
        else:
            if getArg(message) != "r":
                return await m.edit(
                    "Incorrect argument, pass 'r' or 'INT', EX: /q 2"
                )
            reply_message = await client.get_messages(
                message.chat.id,
                message.reply_to_message.id,
                replies=1,
            )
            messages = [reply_message]
    else:
        return await m.edit("Incorrect argument, check quotly module in help section.")
    try:
        if not message:
            return await m.edit("Something went wrong.")

        sticker = await quotify(messages)
        if not sticker[0]:
            await message.reply_text(sticker[1])
            return await m.delete()
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        await m.delete()
        sticker.close()
    except Exception as e:
        await m.edit(
            "Something went wrong while quoting messages,"
            + " this error usually happens when there's a "
            + "message containing something other than text,"
            + " or one of the messages in-between are deleted."
        )
        e = format_exc()
        print(e)


            
@Hiroko.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        name = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1].replace(" ", "%20")
        )
        m = await Hiroko.send_message(message.chat.id, "waito...")
        photo = "https://apis.xditya.me/write?text=" + name
        await Hiroko.send_photo(message.chat.id, photo=photo)
        await m.delete()
    else:
        lol = message.reply_to_message.text
        name = lol.split(None, 0)[0].replace(" ", "%20")
        m = await Hiroko.send_message(message.chat.id, "waito..")
        photo = "https://apis.xditya.me/write?text=" + name
        await Hiroko.send_photo(message.chat.id, photo=photo)
        await m.delete()



