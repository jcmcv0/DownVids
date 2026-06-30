import os

from yt_dlp import YoutubeDL

from core.config import BASE_OPTIONS
from core.utils import normalizar_plataforma
from core.info import obtener_info



def construir_outtmpl(info, carpeta_destino):

    es_playlist = 'entries' in info

    if es_playlist:

        return os.path.join(
            carpeta_destino,
            '%(playlist_title)s',
            '%(title)s.%(ext)s'
        )

    return os.path.join(
        carpeta_destino,
        '%(title)s.%(ext)s'
    )



def crear_hook_progreso(callback=None):

    def hook(d):

        if callback:
            callback(d)

    return hook

def descargar(
    url,
    tipo="video",
    formato="mp4",
    calidad="1080",
    bitrate="320",
    callback=None
):

    info = obtener_info(url)

    extractor = info.get(
        "extractor",
        "otros"
    )

    plataforma = normalizar_plataforma(
        extractor
    )

    carpeta_destino = os.path.join(
        os.getcwd(),
        "downloads",
        plataforma
    )

    os.makedirs(
        carpeta_destino,
        exist_ok=True
    )

    outtmpl = construir_outtmpl(
        info,
        carpeta_destino
    )

    opciones = {
        **BASE_OPTIONS,

        'progress_hooks': [
            crear_hook_progreso(callback)
        ],

        'outtmpl': outtmpl
    }

    if tipo == "video":

        opciones.update({
            'format': f'bestvideo[height<={calidad}]+bestaudio/best',
            'merge_output_format': formato
        })

    else:

        opciones.update({
            'format': 'bestaudio/best',

            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': bitrate,
            }]
        })

    with YoutubeDL(opciones) as ydl:

        ydl.download([url])