import requests
from datetime import date,timedelta
from datetime import datetime


def get_albums_from_artist(url_base,artist_id,token):
    
    headers = {
        "Authorization": token
    }
    offset = 0
    total = 1
    total_items = []
    try:
        while offset < total:
            print(f"Se consulta a partir del album nro: {offset}")
            response = requests.get(url = f"{url_base}artists/{artist_id}/albums?include_groups=album%2Csingle%2Cappears_on%2Ccompilation&market=UY&limit=50&offset={offset}", headers=headers)
            response.raise_for_status()
            response = response.json()
            if total == 1:
                total = response["total"]
                print(f"Fueron encontrados un total de {total} albums")
            items = response["items"]
            starting_offset = response["offset"]
            offset += items.__len__()
            print(f"Guardando en la lista los siguientes {offset - starting_offset} albums")
            total_items.extend(response["items"])
        return total_items
    except requests.exceptions.HTTPError as err:
        print(f"❌ Error de la API: {response.status_code} - {response.text}")
        raise SystemExit(err)

def get_date(date):
    date_time = datetime.strptime(date,"%Y-%m-%d")
    return date_time.date()

def add_filtered_albums_between_dates(filtered_list,album,album_date,newest_date,oldest_date,unique_ids_albums):
    if album_date >= oldest_date and album_date <= newest_date:
        filtered_list.append(album)
        print(f"💾 Album [{album["name"]}] guardado con éxito. Fecha de lanzamiento: {album_date}")
        unique_ids_albums.add(album["id"])
    else:
        print(f"🚫 El álbum [{album["name"]}] no fue guardado. La fecha de lanzamiento: {album_date} no está comprendida entre [{newest_date} - {oldest_date}]")

def get_albums_between_dates(albums,newest_time,oldest_time,unique_ids_albums):
    filtered_albums = []
    for album in albums: 
        if album["id"] not in unique_ids_albums:
            if album["release_date_precision"] == 'day':
                album_date = get_date(album["release_date"])
                add_filtered_albums_between_dates(filtered_albums,album,album_date,newest_time,oldest_time,unique_ids_albums)
            elif album["release_date_precision"] == 'year':
                add_filtered_albums_between_dates(filtered_albums,album,int(album["release_date"]),newest_time.year,oldest_time.year,unique_ids_albums)
            else:
                print(f"⛔ Precision de fecha mal definida. Álbum: [{album["name"]}] - [{album["release_date"]}]")
        else:
            print(f"⛔ El álbum ya fue agregado a las listas. Álbum: [{album["name"]}] - [{album["release_date"]}]")
    return filtered_albums

def get_filtered_albums(albums,newest_time,oldest_time,unique_ids_albums):
    return get_albums_between_dates(albums,newest_time,oldest_time,unique_ids_albums)

def analyze_dates_releases(albums,last_releases,unique_ids_albums):
    today = date.today()
    oldest_time = today - timedelta(days=1825) # 5 años
    print("------------------------------------------------------------------------------------------------------------------")
    print("📈                       ANALIZANDO NUEVOS LANZAMIENTOS DE LOS ÚLTIMOS 5 AÑOS")
    print("------------------------------------------------------------------------------------------------------------------")
    last_releases.extend(get_filtered_albums(albums,today,oldest_time,unique_ids_albums))
