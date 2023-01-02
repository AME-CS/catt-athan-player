import os

video_url = "your_vid_url"

def download_vid(video_url):
    import youtube_dl
    import os
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'athan.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return os.path.abspath("athan.mp3")
    
DEFAULT_ATHAN_PATH = download_vid(video_url)
