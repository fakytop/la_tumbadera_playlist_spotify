import os
import requests
import json

from dotenv import load_dotenv

from methods.get_token import get_token
from methods.get_albums import get_albums_from_artist
from methods.get_albums import analyze_dates_releases
from methods.get_tracks import get_tracks_from_albums
from methods.get_tracks import get_track_info_from_ids
from methods.algorithm import calculate_score  

def export_tracks_to_excel(tracks_info,folder_name):
    import pandas as pd
    excel_data = []
    for track in tracks_info:
        info = {
            "id": track["id"],
            "name": track["name"],
            "popularity": track["popularity"],
            "release_date": track["album"]["release_date"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"]
        }
        excel_data.append(info)
    df = pd.DataFrame(excel_data)
    excel_filepath = os.path.join(folder_name,"last_releases.xlsx")
    df.to_excel(excel_filepath,index=False)


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_ID = os.getenv('SECRET_ID')
URL_BASE = "https://api.spotify.com/v1/"



token = get_token(CLIENT_ID,SECRET_ID)
artists = [ 
    '4PdggFNYwGfjRfkdG5OfES'       # #TocoParaVos
    ,'2rqtqFiCGyzaRSYdgMiMNC'      # 18 Kilates
    ,'27Yc5RzJf27tJfqezJnHY1'      # Agapornis
    ,'1i09cLSfZNYlP8yx7XbK6M'      # Agata Uruguay
    ,'2qmA5QmaGZH3ky4qq25d1m'      # Agus Padilla
    ,'2lT39ZyCy8SWSrTWvWlksN'      # Agustina Nuñez
    ,'2WhGojaMjv4VVn2HQSqrLM'      # Agustin Casanova
    ,'5lekkyDJmqvzCADxRGWQpN'      # Alex Stella
    ,'1gzdihSSQrRPe93050nS0n'      # Alexandra Vila
    ,'3J8GlXHbVSgCF2UPvpPtXM'      # Americo Young
    ,'6Y4g5zwJI7jcRzGLXh0H5d'      # Angela Leiva
    ,'6b0elfFwHQHGkcNUs87yPD'      # Arrancandonga
    ,'474st1ZFIh7IOiUcw9ojHd'      # AX 13
    ,'5Sc57ZJ368JNmUJT4SEU2w'      # Azul
    ,'5NXakitIb9OqlAwfyDgD9M'      # Bien Suave
    ,'10A9ktGErbFGnyn1VplHND'      # Bocha Lozano
    ,'3wzyB2hhQSrqUE4crKX64Y'      # Bola 8
    ,'6FZjAN4tUrVUtL1YcJvUsQ'      # Bryan Alvez
    ,'288dJOiQmxw6pTZ6fqpbiQ'      # CantoParaBailar
    ,'3F4XOLVuGkMDSIGu2Kn33M'      # Carlos Corti y los Muchachos
    ,'76V41O7m8rFTOJllXHBo9G'      # Carol
    ,'7Bl9s8h4F1jcX1aJYHBpfm'      # Chacho Ramos
    ,'1W9l9G6Ao9mm7AhdnHBcsw'      # Chikano Uruguay
    ,'4e3lv5qRgFpdILdEOHchbn'      # Chocolate
    ,'6wJBobCZBqfytvqTgriuuy'      # Como Keda
    ,'6mMF00MGSqk8MT3c31YRSg'      # Como Suena
    ,'5Szju6DGR9hcbFOJeXCN0x'      # Cumbia Rocha
    ,'0cYVTUFGd0A1mKB1jU2hP6'      # Daiami
    ,'0J65S0gB0D1gDEd0hK196k'      # Dame 5
    ,'5pjGkQyoECqaaQLMn9z6he'      # Damian Lescano
    ,'6oWte5YNjECFloePYCVkle'      # Daniel Tata Torres
    ,'4X6BwKYD52c4HHDyUqetfU'      # Denis Elias
    ,'2LI6qhH2fF1uoJpmquvoCn'      # Dessia El Otro
    ,'4AFl787KWUdOe2Ufjd3IqK'      # Didac Torres
    ,'1IYPsxunWpJvDYA1Por8dI'      # Diego Rios
    ,'1fN7fYrsFplBYEOOVxvAvK'      # Diego Salome
    ,'0juoK3n9YuTVWCYxNRaeMw'      # El Gran Maracaibo
    ,'0annXurxTVJKs4QqOqdwGR'      # El Gucci y su Banda
    ,'7tQNgiLNw9eeWJqJ5bCApk'      # El Leon de la Plena
    ,'1LSYfRidvKN3sUXOg8HDWC'      # El Mala
    ,'7HSeegdmjLYRJpkOYIaZIW'      # El Reja
    ,'4nTNHKAVWQyqnvRuBW4N4V'      # El Super Hobby
    ,'7pF1gcXCWyn4xGPPXNWVO5'      # Enzo y La Sub 21
    ,'4LlZgmWlmpRE2BNOXfn5hd'      # Fabricio Mosquera
    ,'3pzjMP43YH7PmEnDAFlO0r'      # Fabrizio
    ,'3xxTHOKHoKoGOVgk1xPUxq'      # Farovi
    ,'4rq5J1gGzgVc1Rw8gdIKGN'      # Feat
    ,'0xJhZwxGtFJ6n5ZAJbVAEe'      # Fede Rojas
    ,'3CoHirtwCpNmEHyoxJoBtg'      # Fer Costa
    ,'5HUPhcBE9Bg1LLnFrhRcOy'      # Fer Silvera
    ,'3R8XhCi6bUcoR1CJx2XASa'      # Flor Alvarez
    ,'1CXffplPsFn0o3kCCHv6IH'      # Flor Sosa
    ,'3OWWlHac5bMtD3A4mIchCs'      # Gabi Arismendi
    ,'1jYImiKsH7041qqudv5oJ2'      # Gerardo Nieto
    ,'5RDuECdgQU0K2pn0vnKAyA'      # Giani Gauna
    ,'77xPFPxusAy6VVAXc6pWFg'      # Gonzalo Castillo
    ,'64WqefdeZwEfh3kyT109mM'      # Grupo Calipso
    ,'4M5Vh0ScxwcwW2nld4pLkP'      # Ilimitados
    ,'30YXApUmvoMSvQ41AuUUNv'      # Javier Leite
    ,'0sDtu16MATPj9OsJ4yhmlu'      # Javier Pacheco
    ,'3QXiKWVF6ze6coCuJcVHSc'      # Jotape
    ,'1eVJpCyT8JStWU3sou78Q7'      # Juan y Rafa
    ,'2WZW6Gsj5R7JlRNFikJvPE'      # Juanjo Morgade
    ,'1I7vbkqIHVffUHHmmXWAYr'      # Julietta
    ,'4GiUBU5qC374SE66G2wYY2'      # Julian Bruno
    ,'7wHbsRbx23UPiHo7sNoXEb'      # Karibe con K
    ,'1QZuAtDYNrk2QMogJulsyq'      # Karina
    ,'7GAayuq6YpBzjGZsqViUvg'      # Katy Bordagorria
    ,'4wld5HDVMVy9I6MnPqjzFH'      # Ke Kumbia
    ,'06Q5VlSAku57lFzyME3HrM'      # Ke Personajes
    ,'23hooy7gxRsySfxxxZasbi'      # KGB Uruguay
    ,'7qyphxox1qgcpTUHbVP5PK'      # Kimba Pintos
    ,'2isxiTW9SDFBPlqJfYm4Ua'      # La Bocha 12
    ,'60cdswzF4ddVcUJKFSQ2yt'      # La Caratula
    ,'15ffMmpL4tbU8By6rURuPe'      # La Cumana
    ,'1j8tYSi1sg9l3MumFojqGj'      # La Decana
    ,'3Pohtvl5MO8eQpaZVOrhUS'      # La Deskarga
    ,'63Q8xmyZacJnzmK7NzVgny'      # La Dupla
    ,'5b0t98sO8PmHcr3eAXcSMg'      # La Fase Buk
    ,'4sXSRSA4DORtoEz8WDqkWa'      # La Dosis
    ,'0YNTZqoGsHjDMFUPbm2jGJ'      # La Furia
    ,'7krUxybhp1bUwFBxpOtmZb'      # La Kuppe
    ,'2JJXJsbTyotc9Rm0KWSTdQ'      # La Misma Cuadra
    ,'5zsJoBmoHM1A6jEoEcNmMv'      # La NT y Los Siniestros
    ,'5TeBsszZQTyqBX4eDHdtNx'      # La Nueva Escuela
    ,'7gHimankGkHEOvQ0UvaZ8t'      # La Pandilla
    ,'07y4PkqTJCaJAjQ1jCKoJx'      # La Penultima
    ,'4oZolC0sCwCAKqsNXfRlVS'      # The La Planta
    ,'75HTvu7Rywwrm4K2yR6xie'      # La Revancha Uruguay
    ,'2dlmYYzcmde3ej5FpNtg7y'      # La Reversa
    ,'4wNFb9W3qEbAgwk0Ln8iea'      # La Revulsiva
    ,'52tZDFZkmb2Q9W0mWY2gJi'      # La Sandonga
    ,'4Yr7TzxjsiFmi51lMt7XrS'      # La SC
    ,'1FxPMQ9A0882eNDx3ZkD6B'      # La T y La M
    ,'2wiC5xzOi2WPiR98XYQSGS'      # La TBT
    ,'5AEQ9NQK8LJSpUzhuJga5u'      # Laguna
    ,'1kyy6AW7C6Rr2jrYwz95Gi'      # Lira
    ,'5v2YVowYeNRB1vK1JTBSP0'      # Los Bembones
    ,'5mLvRBeI5T7w08iWtK7FXu'      # Los Fatales
    ,'6WrhdoSkwNxeTzjtdLfnPU'      # Los Negroni
    ,'6bOZtDVI19rOqC4NWihcea'      # Los Pikantes
    ,'4oLMD76t4pIw2dXsF4VlrI'      # Los Torres
    ,'6Cv7YpJ01y71mdgm4szmU2'      # Los Totora
    ,'6uJKnn4CV4IIop8mg4kCUy'      # Luana
    ,'1AIGPpwjs3zZXT7cJIYEOM'      # Lucas Bunnker
    ,'24QqF0upv6pRO6fMI4jIuL'      # Lucas Corbo
    ,'0WnP62TjkFfRrt52yE8zcX'      # Lucas Sugo
    ,'2G2Z6SpdhR0EtFwu9xsBUG'      # Luciana
    ,'2gHzzL0wGI0XXNuOzcbUe8'      # Lucrecia
    ,'1SDdOa5e5D3XIR2t8Mb3dm'      # L'Autentika
    ,'4d3kmfoZBTuUPSUjgP45uo'      # Lerica
    ,'2dSeDxBzKslmct6a2R4JYZ'      # Majo y la del 13
    ,'0CLDI7ZZQOL43R0C2yfL6V'      # Mala Tuya
    ,'4YBAOrBF9vBB9inOLtpRzp'      # Mano Arriba
    ,'4GepMkTgrIZECoCC55vqjW'      # Marama
    ,'2weGfox1CWg9HmmwDgcjey'      # Marcos da Costa
    ,'50d3BjnDJSg9NHVdSCVoQh'      # Mariam
    ,'6nqh6VtIRmLWvtv6suXdiq'      # Mariano Bermúdez
    ,'63CfZNWQ9yi7UBgby3b2pq'      # Mariel Barboza
    ,'4SgKWjM7cJDCh2aY9H4HZf'      # Marka Akme
    ,'1TndreWtLjfAlywnkm966g'      # Martin Piña
    ,'5jK8mbiICsPLYz9wYOlCdw'      # Martin Quiroga
    ,'2HmIMt98sVFNZYsvHlb96X'      # Martin Segovia
    ,'0XITGSxiogR87aGnlrCEPL'      # Mateo Creciente
    ,'0Ipruw1Cri6pisSi01RPxc'      # Mathi Frame
    ,'6DJKvrwayFW8tm36xcyLxX'      # Mathias Cuadro
    ,'487yb0EEehy2dXIhGg0i9E'      # Mati Costa
    ,'6SGCqG5HEr5gFZR9ct8wID'      # Matias Valdez
    ,'2oPc9LzQ7NP9DIqY70jubf'      # Mawi
    ,'7HW35ytaUKrvvpGoL9wYOz'      # Max Fernandez
    ,'2UnGWnrqDZPjWNVRWj5Mae'      # Maxi Alvarez
    ,'6xvoG4IC2xgLq37QY48fPk'      # Mayonesa
    ,'7zREGj8GMl9UrDa6NPLi0H'      # Meri Deal
    ,'2qVxbJYW5xbslFjhPBGjXY'      # Mica
    ,'48R2gYdPKtfnfKAzhSVPUx'      # Migrantes
    ,'61YAC6zjxT9yLbb0VDcljz'      # Miguel Cufos
    ,'3GKA6SWiCvWlp0aF7e1HPB'      # Miway
    ,'17DxlrTsLMChbltpyHUPzS'      # Monterrojo
    ,'3FBRmXeo3xCgV6TxnLnJsA'      # My Life
    ,'7kqERaGAimGwlTeRWY3ITr'      # Natanael Segovia
    ,'3ihnywVzkqr6nZ7sb9Z4tr'      # Nati Ferrero
    ,'2JTPpvPONEJkgJ28THVqKE'      # NG La Banda
    ,'7rco8qs4mczBpkuIWFeuK6'      # NG Mania
    ,'1OicNKNw1iMMSpFm2VIJwv'      # Nico Conca y su Banda
    ,'0uxYECT7XqHNccQAg5Uhe4'      # Nico Valdi
    ,'51YgtNDifRmwn2hPhAVHCi'      # Nicolas Castillo
    ,'7JIrbjZDpccTaqNKpNKh33'      # Nietos del Futuro
    ,'2XEkeHFfw9gjyrL2Qoi0vj'      # Niko Falero
    ,'2NttQKeTeoxZ64NRTZK0CC'      # Nuestra Banda Ataca
    ,'7Czvx73uua4PB239Dza1Je'      # Olvidate!
    ,'6L2DyVdMndLfvkAelI8vFe'      # ONE PLAY
    ,'6hdAcFnlOI70rcco0TXaH6'      # Pablo Cocina
    ,'59151Fx2qChjbVKmlWcWJb'      # Pal Bailador
    ,'2uot6fY5M4c7qyfEloSoV0'      # The Panas
    ,'5QXX3J6vKeAm8sQ3tyJUy6'      # Pase Libre
    ,'6XIO7MGGTRPdUXqAo1h8bH'      # Paulino
    ,'1aOhJVEGjCbYJLYPCitGdm'      # Pijama Party
    ,'1l6UgL5G16tId4qoYH8qJn'      # Pushi
    ,'5sXtJMLiU5jgZzrPmaj6Gv'      # Renan
    ,'3Bs17Z8VvGiDS6PilLRtG6'      # Richard Santos
    ,'1wkImvL5XLLhrNcmX7sVt4'      # Rodrigo Tapari
    ,'0k9G92e618bqEkc0x55m7f'      # Rolando Paz
    ,'72kCHSLbK0D94Bgpo7G4sJ'      # Romal El Original
    ,'5KQX0Ui06LVm6PApyicRFK'      # Rombai
    ,'2Hxu0Wmd7FUm0euCVInVrN'      # Roze Oficial
    ,'2DDhwTTnjz0HzpMYtcwBZ5'      # Santino
    ,'2TjBEdasWbKTGJnfj5a1ea'      # Seba Pereyra
    ,'6ZZ2DeepA3GpoGU4KwqSlU'      # Luciano Pereyra
    ,'5yUamcZHhXrqRxR768n4YT'      # Seba Torres
    ,'4qywsc4qd533a1CWJUtOR3'      # Siempre Plena
    ,'6LfHVf6hH3gbJaIdX3k8V1'      # Sin Perse
    ,'39x7olLItlZSz0uodtTEeG'      # Sole Ramirez
    ,'54ppqJYv6NrqKz0jCvCWTp'      # Son Ellos
    ,'1vJHAIU4DSvj4XipPK3IR8'      # Sonido Cristal
    ,'29W4Fw8TDGfXD7C9EjJkzc'      # Sonido de la Costa
    ,'3bSypudQFjg4tNIKgoH83Z'      # Sonido Profesional
    ,'1ydZgtUa3wPRwpHNLzz6MV'      # Sonora Borinquen
    ,'5cI70N0pRk5S31TGV4wV0v'      # Sonora Cumanacao
    ,'0R7hVTyBZQ9ApxMtDEAwyL'      # Sonora Palacio
    ,'7s6B9JKCf164EQOQvatr5E'      # Soy Tu Sol
    ,'2gg8RhbAVd4tW7LdZZ5RvR'      # Thian the Producer
    ,'28hVuLtRLgq1HSXM8jI7gA'      # Una Mas
    ,'3AupCsmoHzDH5ghT3hc1DK'      # Urband
    ,'1BfR4gQyjlhLAssULX0wDr'      # Valeria Gau
    ,'04vVNmaKhinxxW4eCJIyX7'      # Valsi
    ,'0rucydKQAXU4U6hxCNm2lr'      # Vanelo
    ,'5XOiPMOBMDm4AYCFRS1e0j'      # Vanesa Britos
    ,'2SId39SaYARSsUE48dGqAE'      # VAPAE
]

last_releases = []
unique_ids_albums = set()
all_albums = []

for artist in artists:
    albums = get_albums_from_artist(URL_BASE,artist,token)
    analyze_dates_releases(albums,last_releases,unique_ids_albums)

last_releases_info = get_tracks_from_albums(last_releases,URL_BASE,token)

tracks_info = get_track_info_from_ids(last_releases_info,URL_BASE,token)

tracks_info.sort(key=calculate_score,reverse=True)
folder_name = "responses_api"
os.makedirs(folder_name,exist_ok=True)

newest_filepath=os.path.join(folder_name,"last_releases.json")

with open(newest_filepath,"w",encoding="utf-8") as f:
    json.dump(tracks_info,f,indent=4,ensure_ascii=False)

export_tracks_to_excel(tracks_info,folder_name)
    
