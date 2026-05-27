import os
import re

from yt_dlp import YoutubeDL


# ==========================================
# CONFIGURACIÓN GLOBAL
# ==========================================

BASE_OPTIONS = {

    'js_runtimes': {
        'node': {}
    },

    'remote_components': ['ejs:github'],

    'restrictfilenames': True
}


FORMATOS_AUDIO = {
    "1": "mp3",
    "2": "m4a",
    "3": "wav",
    "4": "flac",
    "5": "opus"
}


# ==========================================
# UTILIDADES
# ==========================================

def limpiar_nombre(nombre):

    return re.sub(
        r'[<>:"/\\|?*]',
        '_',
        nombre
    )


def normalizar_plataforma(extractor):

    extractor = extractor.lower()

    plataformas = {
        "youtube": "youtube",
        "instagram": "instagram",
        "facebook": "facebook",
        "twitter": "twitter",
        "x": "twitter",
        "tiktok": "tiktok"
    }

    for key, value in plataformas.items():

        if key in extractor:
            return value

    return "otros"


# ==========================================
# INFO DEL VIDEO
# ==========================================

def obtener_info(url):

    with YoutubeDL(BASE_OPTIONS) as ydl:

        return ydl.extract_info(
            url,
            download=False
        )


# ==========================================
# OUTTEMPLATE
# ==========================================

def construir_outtmpl(info, carpeta_destino):

    es_playlist = 'entries' in info

    # Playlist
    if es_playlist:

        return os.path.join(
            carpeta_destino,
            '%(playlist_title)s',
            '%(title)s.%(ext)s'
        )

    # Video único
    return os.path.join(
        carpeta_destino,
        '%(title)s.%(ext)s'
    )


# ==========================================
# OPCIONES VIDEO
# ==========================================

def obtener_opciones_video(outtmpl):

    return {
        **BASE_OPTIONS,

        'format': 'bestvideo+bestaudio/best',

        'merge_output_format': 'mp4',

        'outtmpl': outtmpl
    }


# ==========================================
# OPCIONES AUDIO
# ==========================================

def obtener_opciones_audio(
    formato_audio,
    outtmpl
):

    return {
        **BASE_OPTIONS,

        'format': 'bestaudio/best',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': formato_audio,
            'preferredquality': '320',
        }],

        'outtmpl': outtmpl
    }


# ==========================================
# MENÚ
# ==========================================

def preguntar_tipo_descarga():

    print("\n¿Qué deseas descargar?\n")
    print("1. Video MP4")
    print("2. Audio")

    return input(
        "\nSelecciona opción: "
    )


def preguntar_formato_audio():

    print("\nFormatos disponibles:\n")

    for key, value in FORMATOS_AUDIO.items():

        print(f"{key}. {value}")

    opcion = input(
        "\nSelecciona formato: "
    )

    return FORMATOS_AUDIO.get(
        opcion,
        "mp3"
    )


# ==========================================
# DESCARGA
# ==========================================

def descargar(url):

    # --------------------------
    # Preguntas iniciales
    # --------------------------

    opcion = preguntar_tipo_descarga()

    formato_audio = None

    if opcion == "2":

        formato_audio = preguntar_formato_audio()

    # --------------------------
    # Obtener información
    # --------------------------

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

    # --------------------------
    # Seleccionar opciones
    # --------------------------

    if opcion == "1":

        opciones = obtener_opciones_video(
            outtmpl
        )

    elif opcion == "2":

        opciones = obtener_opciones_audio(
            formato_audio,
            outtmpl
        )

    else:

        print("\nOpción inválida")
        return

    # --------------------------
    # Descargar
    # --------------------------

    with YoutubeDL(opciones) as ydl:

        ydl.download([url])

    print("\nDescarga completada")


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    url = input(
        "Pega la URL del video: "
    )

    try:

        descargar(url)

    except Exception as e:

        print(f"\nOcurrió un error:\n{e}")