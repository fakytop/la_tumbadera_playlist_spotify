import json
import os

import requests
from datetime import date,datetime,timedelta

def get_tracks_info(response,total_tracks_info):
    for album in response["albums"]:
        tracks_from_album = album["tracks"]["items"]
        print(f"🔍 Tracks en el álbum {album['name']}: {len(tracks_from_album)}")
        for track in tracks_from_album:
            total_tracks_info.append(track["id"])

def get_tracks_from_albums(albums,url_base,token):
    headers = {
        "Authorization": token
    }
    total_tracks_info = []
    get_str_albums = ""
    total_albums = albums.__len__()
    print(f"🔍 Total de albums a consultar: {total_albums}")
    counter = 0
    iterator = 0
    for album in albums:
        id_album = album["id"]
        if counter < 20 and counter < total_albums:
            if counter == 0:
                get_str_albums += f"{id_album}"
            else:
                get_str_albums += f",{id_album}"
            counter += 1
        if counter == 20 or counter == total_albums:
            total_albums -= counter
            print(f"🔍 Consultando {counter} albums. Restantes: {total_albums}")
            counter = 0
            response = requests.get(f'{url_base}albums?ids={get_str_albums}&market=UY',headers=headers)
            get_str_albums = ""
            response = response.json()
            get_tracks_info(response, total_tracks_info)
    return total_tracks_info

def get_track_info_from_ids(ids,url_base,token):
    headers = {
        "Authorization": token
    }

    total_tracks_info = []

    get_str_tracks = ""
    total_tracks = ids.__len__()
    print(f"🔍 Total de tracks a consultar: {total_tracks}")
    counter = 0
    for track_id in ids:
        if counter < 50 and counter < total_tracks:
            if counter == 0:
                get_str_tracks += f"{track_id}"
            else:
                get_str_tracks += f",{track_id}"
            counter += 1
        if counter == 50 or counter == total_tracks:
            total_tracks -= counter
            print(f"🔍 Consultando {counter} tracks. Restantes: {total_tracks}")
            counter = 0
            response = requests.get(f'{url_base}tracks?ids={get_str_tracks}&market=UY',headers=headers)
            get_str_tracks = ""
            response = response.json()
            total_tracks_info.extend(response["tracks"])
    return total_tracks_info