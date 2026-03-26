import requests
from datetime import date,datetime,timedelta

def get_tracks_from_albums(albums,url_base,token):
    headers = {
        "Authorization": token
    }
    get_list_albums = []
    total_albums = albums.__len__()
    total_albums_added = 0
    for album in albums:
        id_album = album["id"]
        if id_album not in get_list_albums and get_list_albums.__len__() < 20 :
            get_list_albums.append(id_album)
            