import re


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