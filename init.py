import os
import requests
import json

from dotenv import load_dotenv

from methods.get_token import get_token
from methods.get_albums import get_albums_from_artist
from methods.get_albums import analyze_dates_releases

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_ID = os.getenv('SECRET_ID')
URL_BASE = "https://api.spotify.com/v1/"



token = get_token(CLIENT_ID,SECRET_ID)

albums = get_albums_from_artist(URL_BASE,'6uJKnn4CV4IIop8mg4kCUy',token)

newest_releases = []
last_three_months_releases = []
last_three_years_releases = []

analyze_dates_releases(albums,newest_releases,last_three_months_releases,last_three_years_releases)

folder_name = "responses_api"
os.makedirs(folder_name,exist_ok=True)

newest_filepath=os.path.join(folder_name,"newest_releases.json")
last_months_filepath=os.path.join(folder_name,"last_three_months_releases.json")
last_years_filepath=os.path.join(folder_name,"last_three_years_releases.json")

with open(newest_filepath,"w",encoding="utf-8") as f:
    json.dump(newest_releases,f,indent=4,ensure_ascii=False)
    
with open(last_months_filepath,"w",encoding="utf-8") as f:
    json.dump(last_three_months_releases,f,indent=4,ensure_ascii=False)
    
with open(last_years_filepath,"w",encoding="utf-8") as f:
    json.dump(last_three_years_releases,f,indent=4,ensure_ascii=False)