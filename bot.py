import asyncio
import os
import time
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from config import Config
from database import db
from script import script
from helpers import (
    is_subscribed, 
    get_force_sub_buttons, 
    get_random_image, 
    send_welcome_sticker,
    get_start_buttons,
    get_help_buttons,
    get_about_buttons,
    get_user_info_text,
    format_channels_list
)

# Initialize bot
app = Client(
    "social_downloader_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=Config.MAX_WORKERS
)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    
    # Add user to database
    await db.add_user(user_id, first_name, last_name, username)
    
    # Check force subscription
    if not await is_subscribed(client, user_id):
        channels_list = format_channels_list()
        await message.reply_text(
            script.FORCE_SUB_TXT.format(channels_list),
            reply_markup=get_force_sub_buttons()
        )
        return
    
    # Send welcome sticker
    asyncio.create_task(send_welcome_sticker(client, message.chat.id))
    
    # Wait for sticker to auto-delete
    await asyncio.sleep(Config.STICKER_DELETE_TIME)
    
    # Get random welcome image
    welcome_image = get_random_image()
    
    # Send welcome message with image
    await message.reply_photo(
        photo=welcome_image,
        caption=script.START_TXT.format(message.from_user.mention, "👋"),
        reply_markup=get_start_buttons()
    )

# Group start
@app.on_message(filters.command("start") & filters.group)
async def group_start(client: Client, message: Message):
    await message.reply_text(
        script.GSTART_TXT.format(message.from_user.mention, "👋")
    )

# Help command
@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await message.reply_text(
        script.HELP_TXT,
        reply_markup=get_help_buttons()
    )

# About command
@app.on_message(filters.command("about"))
async def about_command(client: Client, message: Message):
    me = await client.get_me()
    bot_username = me.username
    bot_name = me.first_name
    
    await message.reply_text(
        script.ABOUT_TXT.format(bot_username, bot_name, Config.OWNER_USERNAME),
        reply_markup=get_about_buttons(bot_username),
        disable_web_page_preview=True
    )

# Info command
@app.on_message(filters.command("info"))
async def info_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Check force subscription
    if not await is_subscribed(client, user_id):
        channels_list = format_channels_list()
        await message.reply_text(
            script.FORCE_SUB_TXT.format(channels_list),
            reply_markup=get_force_sub_buttons()
        )
        return
    
    info_text = await get_user_info_text(client, user_id)
    
    # Try to send with profile photo
    try:
        photos = await client.get_profile_photos(user_id, limit=1)
        if photos:
            await message.reply_photo(
                photo=photos[0].file_id,
                caption=info_text
            )
        else:
            await message.reply_text(info_text)
    except:
        await message.reply_text(info_text)

# Broadcast command (admin only)
@app.on_message(filters.command("broadcast") & filters.user(Config.ADMINS))
async def broadcast_command(client: Client, message: Message):
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message
        users = await db.get_all_users()
        total = len(users)
        success = 0
        failed = 0
        start_time = time.time()
        
        status_msg = await message.reply_text("📢 Broadcasting...")
        
        for user_id in users:
            try:
                await broadcast_msg.copy(user_id)
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await broadcast_msg.copy(user_id)
                success += 1
            except:
                failed += 1
            
            if (success + failed) % 50 == 0:
                await status_msg.edit_text(
                    f"📢 Broadcasting...\n\nTotal: {total}\nSuccess: {success}\nFailed: {failed}"
                )
        
        time_taken = round(time.time() - start_time)
        await status_msg.edit_text(
            script.BROADCAST_TXT.format(total, success, failed, time_taken)
        )
    else:
        await message.reply_text("Reply to a message to broadcast!")

# Stats command (admin only)
@app.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def stats_command(client: Client, message: Message):
    total_users = await db.total_users_count()
    await message.reply_text(f"📊 Total Users: {total_users}")

# Callback query handler
@app.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    if data == "check_subscription":
        if await is_subscribed(client, user_id):
            await callback_query.answer("✅ You're subscribed!", show_alert=True)
            
            # Send welcome sticker
            asyncio.create_task(send_welcome_sticker(client, callback_query.message.chat.id))
            
            # Wait for sticker to auto-delete
            await asyncio.sleep(Config.STICKER_DELETE_TIME)
            
            # Get random welcome image
            welcome_image = get_random_image()
            
            # Delete force sub message
            await callback_query.message.delete()
            
            # Send welcome message
            await client.send_photo(
                chat_id=callback_query.message.chat.id,
                photo=welcome_image,
                caption=script.START_TXT.format(callback_query.from_user.mention, "👋"),
                reply_markup=get_start_buttons()
            )
        else:
            await callback_query.answer("❌ Please join all channels first!", show_alert=True)
    
    elif data == "start":
        welcome_image = get_random_image()
        await callback_query.message.edit_media(
            media=callback_query.message.photo,
            caption=script.START_TXT.format(callback_query.from_user.mention, "👋"),
            reply_markup=get_start_buttons()
        )
    
    elif data == "help":
        await callback_query.message.edit_text(
            script.HELP_TXT,
            reply_markup=get_help_buttons()
        )
    
    elif data == "about":
        me = await client.get_me()
        bot_username = me.username
        bot_name = me.first_name
        await callback_query.message.edit_text(
            script.ABOUT_TXT.format(bot_username, bot_name, Config.OWNER_USERNAME),
            reply_markup=get_about_buttons(bot_username),
            disable_web_page_preview=True
        )

# Download handler for URLs
@app.on_message(filters.text & filters.private & ~filters.command(['start', 'help', 'about', 'info', 'broadcast', 'stats']))
async def download_handler(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Check force subscription
    if not await is_subscribed(client, user_id):
        channels_list = format_channels_list()
        await message.reply_text(
            script.FORCE_SUB_TXT.format(channels_list),
            reply_markup=get_force_sub_buttons()
        )
        return
    
    url = message.text.strip()
    
    # Check if it's a valid URL
    if not url.startswith(("http://", "https://")):
        await message.reply_text("❌ Please send a valid URL!")
        return
    
    status_msg = await message.reply_text(script.DOWNLOAD_START)
    
    try:
        # Download options
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        
        # For YouTube, show quality selection
        if 'youtube.com' in url or 'youtu.be' in url:
            buttons = [
                [
                    InlineKeyboardButton("480p", callback_data=f"quality_480_{url}"),
                    InlineKeyboardButton("720p", callback_data=f"quality_720_{url}")
                ],
                [
                    InlineKeyboardButton("1080p", callback_data=f"quality_1080_{url}"),
                    InlineKeyboardButton("4K", callback_data=f"quality_2160_{url}")
                ],
                [InlineKeyboardButton("🎵 MP3", callback_data=f"quality_mp3_{url}")]
            ]
            await status_msg.edit_text(
                "📺 Select video quality:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return
        
        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        await status_msg.edit_text(script.UPLOAD_START)
        
        # Upload the file
        if os.path.exists(filename):
            await client.send_document(
                chat_id=message.chat.id,
                document=filename,
                caption=f"📥 Downloaded by {client.me.mention}"
            )
            
            # Clean up
            os.remove(filename)
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Download failed!")
    
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")

# Quality selection callback
@app.on_callback_query(filters.regex(r"quality_"))
async def quality_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    parts = data.split("_", 2)
    quality = parts[1]
    url = parts[2]
    
    await callback_query.message.edit_text(script.DOWNLOAD_START)
    
    try:
        # Set download options based on quality
        if quality == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }
        else:
            height = quality
            ydl_opts = {
                'format': f'bestvideo[height<={height}]+bestaudio/best[height<={height}]',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
            }
        
        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # For MP3, update filename
            if quality == "mp3":
                filename = filename.rsplit('.', 1)[0] + '.mp3'
        
        await callback_query.message.edit_text(script.UPLOAD_START)
        
        # Upload the file
        if os.path.exists(filename):
            if quality == "mp3":
                await client.send_audio(
                    chat_id=callback_query.message.chat.id,
                    audio=filename,
                    caption=f"🎵 Downloaded by {client.me.mention}"
                )
            else:
                await client.send_video(
                    chat_id=callback_query.message.chat.id,
                    video=filename,
                    caption=f"📹 Quality: {quality}\nDownloaded by {client.me.mention}"
                )
            
            # Clean up
            os.remove(filename)
            await callback_query.message.delete()
        else:
            await callback_query.message.edit_text("❌ Download failed!")
    
    except Exception as e:
        await callback_query.message.edit_text(f"❌ Error: {str(e)}")

# Create downloads directory
os.makedirs("downloads", exist_ok=True)

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
