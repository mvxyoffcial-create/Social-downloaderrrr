# Telegram Social Media Downloader Bot

A powerful Telegram bot that can download videos and audio from various social media platforms including YouTube, Instagram, TikTok, Facebook, and more!

## Features

- 📥 Download videos from multiple social media platforms
- 🎵 Download audio/MP3 from YouTube
- 📺 YouTube quality selection (480p, 720p, 1080p, 4K)
- 🔒 Force subscription to channels
- 👤 User info command
- 📢 Broadcast messages to all users
- 📊 User statistics
- 🎨 Random welcome images
- 🎭 Animated welcome sticker
- 💾 MongoDB database integration
- ⚡ Up to 500 workers support

## Supported Platforms

- YouTube
- Instagram
- TikTok
- Facebook
- Twitter/X
- And many more!

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher
2. A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
3. API ID and API Hash from [my.telegram.org](https://my.telegram.org)
4. MongoDB database (you can use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) for free)

### Installation

1. Clone or extract this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file or set these environment variables:

   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   DATABASE_URI=your_mongodb_uri
   DATABASE_NAME=telegram_bot
   OWNER_ID=your_telegram_user_id
   OWNER_USERNAME=@YourUsername
   ADMINS=admin_id1 admin_id2
   ```

### Configuration

Edit `config.py` to customize:
- Force subscription channels
- Welcome images
- Sticker file ID
- Maximum workers
- Other settings

### Running the Bot

```bash
python bot.py
```

### Deployment

#### Heroku
1. Create a new Heroku app
2. Add Python buildpack
3. Set environment variables in Heroku dashboard
4. Connect to GitHub or deploy manually

#### VPS/Server
1. Upload files to your server
2. Install dependencies
3. Set environment variables
4. Run with `python bot.py` or use process manager like PM2

## Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/about` - About the bot
- `/info` - Get your user information
- `/broadcast` - Broadcast message (Admin only)
- `/stats` - Show user statistics (Admin only)

## Usage

1. Start the bot with `/start`
2. Join the required channels
3. Send any social media link
4. For YouTube: Select quality
5. Get your downloaded file!

## Developer

Created by [@Venuboyy](https://t.me/Venuboyy)

## Support

Join our channels:
- [@zerodev2](https://t.me/zerodev2)
- [@mvxyoffcail](https://t.me/mvxyoffcail)

## License

This project is for educational purposes only. Make sure to comply with the terms of service of the platforms you're downloading from.

## Notes

- Make sure FFmpeg is installed on your system for video/audio processing
- The bot requires sufficient storage space for temporary downloads
- Keep your API credentials secure and never share them
- Respect rate limits and platform terms of service
