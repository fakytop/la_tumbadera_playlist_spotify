import requests

def add_albums(total_items,items):
    total_items.extend(items)

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
            add_albums(total_items,response["items"])
        return total_items
    except requests.exceptions.HTTPError as err:
        print(f"❌ Error de la API: {response.status_code} - {response.text}")
        raise SystemExit(err)