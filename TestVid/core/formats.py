from core.config import (
    FORMATOS_AUDIO,
    FORMATOS_VIDEO
)



def obtener_calidades_video(info):

    formatos = info.get("formats", [])

    resoluciones = set()

    for formato in formatos:

        height = formato.get("height")

        if height:
            resoluciones.add(f"{height}p")

    resoluciones = sorted(
        resoluciones,
        key=lambda x: int(x.replace("p", ""))
    )

    return resoluciones



def obtener_formatos_audio():

    return list(
        FORMATOS_AUDIO.keys()
    )



def obtener_formatos_video():

    return list(
        FORMATOS_VIDEO.keys()
    )