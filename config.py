import os
from os import environ

class Config:
    # Bot Configuration
    API_ID = "20288994"
    API_HASH = "d702614912f1ad370a0d18786002adbf"
    BOT_TOKEN = "7958640544:AAGQSUlrLk8WL7aqfBSusVsMvP-E7LwlZ5w"
    
    # Database Configuration
    DATABASE_URI = "mongodb+srv://Zerobothost:zero8907@cluster0.szwdcyb.mongodb.net/?appName=Cluster0"
    DATABASE_NAME = "telegram_bot"
    
    # Force Subscribe Channels
    FORCE_SUB_CHANNELS = [
        "@zerodev2",
        "@mvxyoffcail"
    ]
    
    # Owner/Developer
    OWNER_ID = "8498741978"
    OWNER_USERNAME = "@Venuboyy"
    
    # Welcome Images
    WELCOME_IMAGE = "https://i.ibb.co/pr2H8cwT/img-8312532076.jpg"
    RANDOM_IMAGE_API = "https://api.aniwallpaper.workers.dev/random?type=girl"
    
    # Welcome Sticker
    WELCOME_STICKER = "CAACAgIAAxkBAAEQZtFpgEdROhGouBVFD3e0K-YjmVHwsgACtCMAAphLKUjeub7NKlvk2TgE"
    
    # Workers
    MAX_WORKERS = "500"
    
    # Bot Settings
    STICKER_DELETE_TIME = "2"
    
    # Admin IDs for broadcast
    ADMINS = 8498741978
