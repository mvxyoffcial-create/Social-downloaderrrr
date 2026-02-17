import requests
import asyncio
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied
from config import Config
from script import script

async def is_subscribed(client: Client, user_id: int):
    """Check if user is subscribed to all force sub channels"""
    for channel in Config.FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ["kicked", "left"]:
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Error checking subscription for {channel}: {e}")
            return False
    return True

def get_force_sub_buttons():
    """Generate inline buttons for force subscription channels"""
    buttons = []
    for i, channel in enumerate(Config.FORCE_SUB_CHANNELS, 1):
        channel_name = channel.replace("@", "")
        buttons.append([InlineKeyboardButton(f"📢 Join Channel {i}", url=f"https://t.me/{channel_name}")])
    
    buttons.append([InlineKeyboardButton("✅ ɪ ᴊᴏɪɴᴇᴅ", callback_data="check_subscription")])
    return InlineKeyboardMarkup(buttons)

def get_random_image():
    """Get random image from API"""
    try:
        response = requests.get(Config.RANDOM_IMAGE_API, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('url', Config.WELCOME_IMAGE)
    except:
        pass
    return Config.WELCOME_IMAGE

async def send_welcome_sticker(client: Client, chat_id: int):
    """Send welcome sticker and auto-delete after delay"""
    try:
        sticker_msg = await client.send_sticker(
            chat_id=chat_id,
            sticker=Config.WELCOME_STICKER
        )
        await asyncio.sleep(Config.STICKER_DELETE_TIME)
        await sticker_msg.delete()
    except Exception as e:
        print(f"Error sending sticker: {e}")

def get_start_buttons():
    """Get start command inline buttons"""
    buttons = [
        [
            InlineKeyboardButton("ℹ️ ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{Config.OWNER_USERNAME.replace('@', '')}")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def get_help_buttons():
    """Get help command inline buttons"""
    buttons = [
        [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="start")],
    ]
    return InlineKeyboardMarkup(buttons)

def get_about_buttons(bot_username):
    """Get about command inline buttons"""
    buttons = [
        [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="start")],
    ]
    return InlineKeyboardMarkup(buttons)

async def get_user_info_text(client: Client, user_id: int):
    """Generate user info text"""
    try:
        user = await client.get_users(user_id)
        first_name = user.first_name or "None"
        last_name = user.last_name or "None"
        username = f"@{user.username}" if user.username else "None"
        dc_id = user.dc_id or "Unknown"
        
        return script.INFO_TXT.format(
            first_name,
            last_name,
            user_id,
            dc_id,
            username,
            user_id
        )
    except Exception as e:
        return f"Error getting user info: {e}"

def format_channels_list():
    """Format channels list for force sub message"""
    channels_text = ""
    for i, channel in enumerate(Config.FORCE_SUB_CHANNELS, 1):
        channels_text += f"{i}. {channel}\n"
    return channels_text
