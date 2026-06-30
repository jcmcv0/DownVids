import subprocess



def actualizar_ytdlp():

    try:

        subprocess.run(
            [
                "pip",
                "install",
                "-U",
                "yt-dlp"
            ],
            check=True
        )

        return True

    except Exception:

        return False