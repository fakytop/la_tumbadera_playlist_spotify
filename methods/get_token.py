import requests
def get_token(CLIENT_ID,SECRET_ID):
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": SECRET_ID
    }

    try:
        response = requests.post(url="https://accounts.spotify.com/api/token",headers=headers,data=data)
        response.raise_for_status()
        response_json = response.json()
        return f"{response_json["token_type"]} {response_json["access_token"]}"
    except requests.exceptions.HTTPError as err:
        print(f"❌ Error de la API: {response.status_code} - {response.text}")
        raise SystemExit(err)