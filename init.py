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
artists = [ 
    '6uJKnn4CV4IIop8mg4kCUy' # Luana
    ,'2WZW6Gsj5R7JlRNFikJvPE' # Juanjo Morgade
    ,'2UnGWnrqDZPjWNVRWj5Mae' # Maxi Alvarez
    ,'5TeBsszZQTyqBX4eDHdtNx' # La Nueva Escuela
    ,'4wNFb9W3qEbAgwk0Ln8iea' # La Revulsiva
    ,'4sXSRSA4DORtoEz8WDqkWa' # La Dosis
    ,'3Pohtvl5MO8eQpaZVOrhUS' # La Deskarga
    ,'6WrhdoSkwNxeTzjtdLfnPU' # Los Negroni
    ,'4X6BwKYD52c4HHDyUqetfU' # Denis Elias
    ,'5pjGkQyoECqaaQLMn9z6he' # Damian Lescano
    ,'0annXurxTVJKs4QqOqdwGR' # El Gucci
    ,'2weGfox1CWg9HmmwDgcjey' # Marcos Da Costa
    ,'6nqh6VtIRmLWvtv6suXdiq' # Mariano Bermúdez
    ,'6bOZtDVI19rOqC4NWihcea' # Los Pikantes
]

newest_releases = []
last_month_releases = []
last_year_releases = []
unique_ids_albums = set()

for artist in artists:
    albums = get_albums_from_artist(URL_BASE,artist,token)
    analyze_dates_releases(albums,newest_releases,last_month_releases,last_year_releases,unique_ids_albums)


folder_name = "responses_api"
os.makedirs(folder_name,exist_ok=True)

newest_filepath=os.path.join(folder_name,"newest_releases.json")
last_months_filepath=os.path.join(folder_name,"last_month.json")
last_years_filepath=os.path.join(folder_name,"last_year.json")

with open(newest_filepath,"w",encoding="utf-8") as f:
    json.dump(newest_releases,f,indent=4,ensure_ascii=False)
    
with open(last_months_filepath,"w",encoding="utf-8") as f:
    json.dump(last_month_releases,f,indent=4,ensure_ascii=False)
    
with open(last_years_filepath,"w",encoding="utf-8") as f:
    json.dump(last_year_releases,f,indent=4,ensure_ascii=False)