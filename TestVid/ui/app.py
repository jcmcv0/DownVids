import threading

import customtkinter as ctk

from core.downloader import descargar


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



def iniciar_app():

    app = ctk.CTk()

    app.title("Video Downloader")

    app.geometry("700x550")

    # =====================================
    # VARIABLES
    # =====================================

    tipo_var = ctk.StringVar(value="video")

    formato_video_var = ctk.StringVar(value="mp4")

    formato_audio_var = ctk.StringVar(value="mp3")

    calidad_var = ctk.StringVar(value="1080")

    bitrate_var = ctk.StringVar(value="320")

    # =====================================
    # TÍTULO
    # =====================================

    titulo = ctk.CTkLabel(
        app,
        text="Video Downloader",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=20)

    # =====================================
    # URL
    # =====================================

    url_entry = ctk.CTkEntry(
        app,
        width=600,
        height=40,
        placeholder_text="Pega la URL aquí"
    )

    url_entry.pack(pady=10)

    # =====================================
    # TIPO
    # =====================================

    tipo_frame = ctk.CTkFrame(app)

    tipo_frame.pack(pady=10)

    video_radio = ctk.CTkRadioButton(
        tipo_frame,
        text="Video",
        variable=tipo_var,
        value="video"
    )

    video_radio.pack(side="left", padx=20)

    audio_radio = ctk.CTkRadioButton(
        tipo_frame,
        text="Audio",
        variable=tipo_var,
        value="audio"
    )

    audio_radio.pack(side="left", padx=20)

    # =====================================
    # VIDEO OPTIONS
    # =====================================

    video_frame = ctk.CTkFrame(app)

    video_frame.pack(pady=10)

    calidad_menu = ctk.CTkOptionMenu(
        video_frame,
        variable=calidad_var,
        values=[
            "360",
            "720",
            "1080",
            "1440",
            "2160"
        ]
    )

    calidad_menu.pack(side="left", padx=10)

    formato_video_menu = ctk.CTkOptionMenu(
        video_frame,
        variable=formato_video_var,
        values=[
            "mp4",
            "mkv",
            "webm"
        ]
    )

    formato_video_menu.pack(side="left", padx=10)

    # =====================================
    # AUDIO OPTIONS
    # =====================================

    audio_frame = ctk.CTkFrame(app)

    audio_frame.pack(pady=10)

    formato_audio_menu = ctk.CTkOptionMenu(
        audio_frame,
        variable=formato_audio_var,
        values=[
            "mp3",
            "m4a",
            "wav",
            "flac",
            "opus"
        ]
    )

    formato_audio_menu.pack(side="left", padx=10)

    bitrate_menu = ctk.CTkOptionMenu(
        audio_frame,
        variable=bitrate_var,
        values=[
            "128",
            "192",
            "256",
            "320"
        ]
    )

    bitrate_menu.pack(side="left", padx=10)

    # =====================================
    # PROGRESO
    # =====================================

    progreso = ctk.CTkProgressBar(
        app,
        width=500
    )

    progreso.pack(pady=20)

    progreso.set(0)

    estado = ctk.CTkLabel(
        app,
        text="Esperando descarga..."
    )

    estado.pack()

    # =====================================
    # CALLBACK PROGRESO
    # =====================================

    def progreso_hook(d):

        if d['status'] == 'downloading':

            porcentaje = d.get('_percent_str', '0%')

            porcentaje = porcentaje.replace('%', '').strip()

            try:

                porcentaje_float = float(porcentaje)

                progreso.set(
                    porcentaje_float / 100
                )

                estado.configure(
                    text=f"Descargando... {porcentaje}%"
                )

            except Exception:
                pass

        elif d['status'] == 'finished':

            progreso.set(1)

            estado.configure(
                text="Procesando archivo..."
            )

    # =====================================
    # DESCARGA
    # =====================================

    def iniciar_descarga():

        url = url_entry.get()

        if not url:

            estado.configure(
                text="Debes ingresar una URL"
            )

            return

        estado.configure(
            text="Iniciando descarga..."
        )

        progreso.set(0)

        def tarea():

            try:

                descargar(
                    url=url,
                    tipo=tipo_var.get(),
                    formato=(
                        formato_video_var.get()
                        if tipo_var.get() == "video"
                        else formato_audio_var.get()
                    ),
                    calidad=calidad_var.get(),
                    bitrate=bitrate_var.get(),
                    callback=progreso_hook
                )

                estado.configure(
                    text="Descarga completada"
                )

            except Exception as e:

                estado.configure(
                    text=f"Error: {e}"
                )

        threading.Thread(
            target=tarea,
            daemon=True
        ).start()

    # =====================================
    # BOTÓN
    # =====================================

    boton = ctk.CTkButton(
        app,
        text="DESCARGAR",
        width=250,
        height=45,
        command=iniciar_descarga
    )

    boton.pack(pady=20)

    app.mainloop()