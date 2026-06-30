from yt_dlp import YoutubeDL

from core.config import BASE_OPTIONS



def obtener_info(url):

    with YoutubeDL(BASE_OPTIONS) as ydl:

        return ydl.extract_info(
            url,
            download=False
        )