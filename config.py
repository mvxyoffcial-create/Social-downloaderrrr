import os
from os import environ

class Config:
    # Bot Configuration
    API_ID = int(environ.get("API_ID", "12345678"))
    API_HASH = environ.get("API_HASH", "your_api_hash_here")
    BOT_TOKEN = environ.get("BOT_TOKEN", "your_bot_token_here")
    
    # Database Configuration
    DATABASE_URI = environ.get("DATABASE_URI", "mongodb+srv://username:password@cluster.mongodb.net/")
    DATABASE_NAME = environ.get("DATABASE_NAME", "telegram_bot")
    
    # Force Subscribe Channels
    FORCE_SUB_CHANNELS = [
        "@zerodev2",
        "@mvxyoffcail"
    ]
    
    # Owner/Developer
    OWNER_ID = int(environ.get("OWNER_ID", "1234567890"))
    OWNER_USERNAME = environ.get("OWNER_USERNAME", "@Venuboyy")
    
    # Welcome Images
    WELCOME_IMAGE = environ.get("WELCOME_IMAGE", "https://i.ibb.co/pr2H8cwT/img-8312532076.jpg")
    RANDOM_IMAGE_API = environ.get("RANDOM_IMAGE_API", "https://api.aniwallpaper.workers.dev/random?type=girl")
    
    # Welcome Sticker
    WELCOME_STICKER = environ.get("WELCOME_STICKER", "CAACAgIAAxkBAAEQZtFpgEdROhGouBVFD3e0K-YjmVHwsgACtCMAAphLKUjeub7NKlvk2TgE")
    
    # Workers
    MAX_WORKERS = int(environ.get("MAX_WORKERS", "500"))
    
    # Bot Settings
    STICKER_DELETE_TIME = int(environ.get("STICKER_DELETE_TIME", "2"))  # seconds
    
    # Admin IDs for broadcast
    ADMINS = list(set(int(x) for x in environ.get("ADMINS", "1234567890").split()))
    ADMINS.append(OWNER_ID)
