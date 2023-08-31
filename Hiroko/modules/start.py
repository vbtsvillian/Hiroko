import asyncio
import random
from time import time
from datetime import datetime
from config import BOT_USERNAME, OWNER_ID
from pyrogram import filters, Client
from Hiroko import Hiroko
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Hiroko.Helper.database.chatsdb import add_served_chat
from Hiroko.Helper.database.usersdb import add_served_user
from Hiroko.modules.text import SHORTENER_TEXT, ADMINS_TEXT, GITHUB_TEXT, FUN_TEXT, MISC_TEXT, NEKOS_TEXT, GAMES_TEXT, CHATGPT_TEXT, CHATBOT_TEXT, INSTATUS_TEXT, AFK_TEXT, ACTION_TEXT         

# ------------------------------------------------------------------------------- #

START_IMG = (
"https://graph.org/file/3f7abc44fe9f39a1eb4fe.jpg",
"https://graph.org/file/81ecdf048901982ecc8d8.jpg",
"https://graph.org/file/a9418e9ea5d8c3c44c996.jpg",
"https://graph.org/file/c24c72f854e85fd43cf1f.jpg",
"https://graph.org/file/8c385a92033f329da20ff.jpg",
"https://graph.org/file/b41c0122caf1ef151f385.jpg",
"https://graph.org/file/e6ab29634f70735fe82aa.jpg",
"https://graph.org/file/329751a8e6435de02204e.jpg",

)



# ------------------------------------------------------------------------------- #

START_TEXT = """
**ʜᴇʏ ᴛʜᴇʀᴇ [{}](tg://user?id={}) ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !**
━━━━━━━━━━━━━━━━━━━━━━**
๏ ɪ ᴀᴍ ˹ᴠɪʟʟɪᴀɴ ꝛᴏʙᴏᴛ˼ ᴀɴᴅ ɪ ʜᴀᴠᴇ sᴘᴇᴄɪᴀʟ ғᴇᴀᴛᴜʀᴇs
๏ ɪ ᴀᴍ ᴅɪғғᴇʀᴇɴᴛ ғʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛs

๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs**
"""


# ------------------------------------------------------------------------------- #

HELP_TEXT = """**
» ˹ᴠɪʟʟɪᴀɴ ꝛᴏʙᴏᴛ˼ ᴄᴏᴏʟ ᴏʀ ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs 

» ᴀʟʟ ᴏꜰ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ / ᴏʀ !
» ɪꜰ ʏᴏᴜ ɢᴏᴛ ᴀɴʏ ɪssᴜᴇ ᴏʀ ʙᴜɢ ɪɴ ᴀɴʏ ᴄᴏᴍᴍᴀɴᴅ ᴘʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴀᴛ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](https://t.me/TheNixaSupport)**
ㅤㅤㅤㅤㅤㅤ
‣<code> /start</code> : **ꜱᴛᴀʀᴛꜱ ᴍᴇ | ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ʏᴏᴜ'ᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴅᴏɴᴇ ɪᴛ.**
‣<code> /donate</code> : **sᴜᴘᴘᴏʀᴛ ᴍᴇ ʙʏ ᴅᴏɴᴀᴛɪɴɢ ꜰᴏʀ ᴍʏ ʜᴀʀᴅᴡᴏʀᴋ.**
"""



# ------------------------------------------------------------------------------- #

hiroko_buttons = [              
                [
                    InlineKeyboardButton("ᴀғᴋ", callback_data="maintainer_"),   
                    InlineKeyboardButton("ᴀᴅᴍɪɴs", callback_data="admins_"),
                    InlineKeyboardButton("ғᴜɴ", callback_data="fun_")
                ],
                [
                    InlineKeyboardButton("ɢɪᴛʜᴜʙ", callback_data="github_"),   
                    InlineKeyboardButton("ɪɴsᴛᴀᴛᴜs", callback_data="instatus_"),
                    InlineKeyboardButton("ɴᴇᴋᴏs", callback_data="nekos_")
                ],
                [
                    InlineKeyboardButton("ᴄʜᴀᴛʙᴏᴛ", callback_data="maintainer_"),   
                    InlineKeyboardButton("ᴍɪsᴄ", callback_data="misc_"),
                    InlineKeyboardButton("sʜᴏʀᴛᴇɴᴇʀ", callback_data="shortener_")
                ],
                [
                    InlineKeyboardButton("ɢᴀᴍᴇs", callback_data="action_"),   
                    InlineKeyboardButton("ᴄʜᴀᴛɢᴘᴛ", callback_data="chatgpt_"),
                    InlineKeyboardButton("ᴀᴄᴛɪᴏɴ", callback_data="action_")
                ],             
                [
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="home_"),
                    InlineKeyboardButton("⟲ ᴄʟᴏꜱᴇ ⟳", callback_data="close_data")
                ]
                ]


back_buttons  = [[
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="help_"),                    
                ]]

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client: Client, message: Message):    
        get_me = await client.get_me()
        BOT_USERNAME = get_me.username
        buttons = [
            [
                InlineKeyboardButton("☆ 𝑨𝒅𝒅 𝑴𝒆 𝑻𝒐 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑 ☆", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
            [
                InlineKeyboardButton("🌼𝑮𝒓𝒐𝒖𝒑🌼", url="https://t.me/HLV_NETWORK"),
                InlineKeyboardButton("🏡𝑶𝒇𝒇𝒊𝒄𝒆🏡", url=f"https://t.me/villen_012"),
            ],
            [
                InlineKeyboardButton("🌷𝑯𝒆𝒍𝒑🌷", callback_data="help_")
            ]    
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(START_IMG),
            caption=START_TEXT.format(message.from_user.first_name, message.from_user.id),
            reply_markup=reply_markup
        )
        await add_served_user(message.from_user.id)            
        await add_served_chat(message.chat.id)


# ------------------------------------------------------------------------------- #

@Hiroko.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data=="home_":
        buttons =  [
            [
                InlineKeyboardButton("☆ 𝑨𝒅𝒅 𝑴𝒆 𝑻𝒐 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑 ☆", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
            [
                InlineKeyboardButton("🌼𝑮𝒓𝒐𝒖𝒑🌼", url="https://t.me/HLV_NETWORK"),
                InlineKeyboardButton("🏡𝑶𝒇𝒇𝒊𝒄𝒆🏡", url=f"https://t.me/villen_012"),
            ],
            [
                InlineKeyboardButton("🌷𝑯𝒆𝒍𝒑🌷", callback_data="help_")
            ]    
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                START_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #
        
    elif query.data=="help_":        
        reply_markup = InlineKeyboardMarkup(hiroko_buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

  
# ------------------------------------------------------------------------------- #

    elif query.data=="afk_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                AFK_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

  
# ------------------------------------------------------------------------------- #

    elif query.data=="admins_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                ADMINS_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="fun_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                FUN_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass 


# ------------------------------------------------------------------------------- #

    elif query.data=="github_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                GITHUB_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="instatus_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                INSTATUS_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="nekos_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                NEKOS_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="chatbot_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                CHATBOT_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="misc_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                MISC_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="shortener_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                SHORTENER_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="games_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                GAMES_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="chatgpt_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                CHATGPT_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="action_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                ACTION_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="maintainer_":
            await query.answer(("sᴏᴏɴ.... \n ʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ "), show_alert=True)

  
# ------------------------------------------------------------------------------- #
 
    elif query.data=="close_data":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass
          

# ------------------------------------------------------------------------------- #


