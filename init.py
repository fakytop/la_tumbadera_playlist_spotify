import os
import requests
import json
from dotenv import load_dotenv

from methods.get_token import get_token
from methods.get_albums import get_albums_from_artist

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_ID = os.getenv('SECRET_ID')
URL_BASE = "https://api.spotify.com/v1/"



token = get_token(CLIENT_ID,SECRET_ID)

albums = get_albums_from_artist(URL_BASE,'6uJKnn4CV4IIop8mg4kCUy',token)
# print(json.dumps(albums,indent=4,ensure_ascii=False))
