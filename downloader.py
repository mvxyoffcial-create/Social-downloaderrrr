import os
import yt_dlp
from config import Config

class Downloader:
    """Handle downloads from various platforms"""
    
    @staticmethod
    def get_ydl_opts(url, quality=None, audio_only=False):
        """Get yt-dlp options based on URL and requirements"""
        
        # Base options
        opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
        }
        
        # Instagram specific options
        if 'instagram.com' in url or 'instagr.am' in url:
            opts.update({
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                }
            })
            
            # Add cookies if available
            if os.path.exists(Config.COOKIES_FILE):
                opts['cookiefile'] = Config.COOKIES_FILE
            
            # Add credentials if provided
            if Config.INSTAGRAM_USERNAME and Config.INSTAGRAM_PASSWORD:
                opts['username'] = Config.INSTAGRAM_USERNAME
                opts['password'] = Config.INSTAGRAM_PASSWORD
        
        # TikTok specific options
        elif 'tiktok.com' in url or 'vm.tiktok.com' in url:
            opts.update({
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            })
            if os.path.exists(Config.COOKIES_FILE):
                opts['cookiefile'] = Config.COOKIES_FILE
        
        # YouTube specific options
        elif 'youtube.com' in url or 'youtu.be' in url:
            if audio_only:
                opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            elif quality:
                height = quality.replace('p', '')
                opts['format'] = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
                opts['merge_output_format'] = 'mp4'
            else:
                opts['format'] = 'bestvideo+bestaudio/best'
                opts['merge_output_format'] = 'mp4'
        
        # Twitter/X specific options
        elif 'twitter.com' in url or 'x.com' in url:
            opts.update({
                'format': 'best',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            })
            if os.path.exists(Config.COOKIES_FILE):
                opts['cookiefile'] = Config.COOKIES_FILE
        
        # Facebook specific options
        elif 'facebook.com' in url or 'fb.watch' in url:
            opts.update({
                'format': 'best',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            })
            if os.path.exists(Config.COOKIES_FILE):
                opts['cookiefile'] = Config.COOKIES_FILE
        
        # Default for other platforms
        else:
            opts['format'] = 'best'
        
        return opts
    
    @staticmethod
    def download(url, quality=None, audio_only=False):
        """Download video/audio from URL"""
        try:
            opts = Downloader.get_ydl_opts(url, quality, audio_only)
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # For MP3, update filename
                if audio_only:
                    filename = filename.rsplit('.', 1)[0] + '.mp3'
                
                return filename, info.get('title', 'Download')
        
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            
            # Instagram specific error handling
            if 'instagram' in url.lower():
                if 'rate-limit' in error_msg or 'login required' in error_msg:
                    raise Exception(
                        "❌ Instagram Error!\n\n"
                        "Instagram requires authentication. Please:\n"
                        "1. Add Instagram credentials (username/password), OR\n"
                        "2. Export cookies from your browser\n\n"
                        "Contact @Venuboyy for setup help."
                    )
            
            # Generic error
            raise Exception(f"Download failed: {error_msg}")
        
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
    
    @staticmethod
    def get_info(url):
        """Get video info without downloading"""
        try:
            opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            return None
