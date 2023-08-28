import requests
import os
import psutil
import time
import obspython as obs

previous_title = None

def get_episode_title():
    vlc_process = None
    # Buscar el proceso de VLC en ejecución
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'vlc.exe':  # Cambia el nombre del proceso según tu sistema operativo
            vlc_process = process
            break

    if vlc_process:
        # Obtener la lista de archivos abiertos por VLC
        open_files = vlc_process.open_files()

        if open_files:            
            # Tomar el primer archivo South Park abierto por VLC
            for file in open_files:
                if "Park" in file.path:
                    file_path = file.path
                    break


            # Obtener el nombre del archivo sin la ruta y la extensión
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            #he cambiado file_path por filename pa saber de donde viene
            return file_name

    return None


def change_stream_title():

    episode_title = get_episode_title()
    global previous_title

    if previous_title != episode_title:
        previous_title = episode_title

        # Aquí debes reemplazar 'YOUR_TWITCH_CHANNEL' con tu nombre de usuario de Twitch y 'YOUR_TWITCH_TOKEN' con tu token de acceso a la API de Twitch.
        url = "https://api.twitch.tv/helix/channels?broadcaster_id=???????????"
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            "Client-ID": "???????????????????????",
            "Authorization": "Bearer ????????????????????????",
            "Content-Type": "application/json"
        }

        # Envía una solicitud a la API de Twitch para cambiar el título de la transmisión.
        try:
            response = requests.patch(url, headers=headers, json={"title": episode_title})
            response.raise_for_status()  # Genera una excepción si hay un error de estado en la respuesta
            print("El título de la transmisión se cambió con éxito.")
        except requests.exceptions.RequestException as e:
            print("Hubo un error en la solicitud a la API de Twitch:", e)
    else:
        print("Mismo episodio")


def script_description():
    return "Script para cambiar automáticamente el título de la transmisión en OBS."

#def script_update(settings):
#   pass

def script_load(settings):
    obs.timer_add(change_stream_title, 1325930)  # Cambia el título cada XX000 segundos (ajusta este valor según tus necesidades).

def script_unload():
    obs.timer_remove(change_stream_title)