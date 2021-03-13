import requests
import json

# Function to create program in one click
def getProgramData(tmdb_id, media_type):

    params = dict(api_key="69cce8dbf435199baf4ab9dfcb63616d", language="fr-FR")

    if(media_type=='tv'):
        req = requests.get("https://api.themoviedb.org/3/tv/{}".format(tmdb_id) , params)
        data = json.loads(req.content)

        origins = [ network['origin_country'] for network in data['networks'] ]
        list_networks = [ network['name'] for network in data['networks'] ]

        name = data['name']
        original_name = data['original_name']
        last_air_date = data['last_air_date']
        first_air_date = data['first_air_date']
        program_format = 1

    elif(media_type=='movie'):
        req = requests.get("https://api.themoviedb.org/3/movie/{}".format(tmdb_id) , params)
        data = json.loads(req.content)

        origins = [ production_company['name'] for production_company in data['production_countries'] ]
        list_networks = [ production_company['name'] for production_company in data['production_companies'] ]

        name = data['title']
        original_name = data['original_title']
        last_air_date = data['release_date']
        first_air_date = data['release_date']
        program_format = 0

    else:

        return False


    
    list_genres = [ genre['name'] for genre in data['genres'] ]

    program = dict(tmdb_id=tmdb_id,
                    name=name,
                    format=program_format,
                    homepage_link=data['homepage'],
                    source=", ".join(list_networks),
                    origin_country=", ".join(origins),
                    original_name=original_name,
                    synopsis=data['overview'],
                    poster_path=data['poster_path'],
                    tags=", ".join(list_genres),
                    last_air_date=last_air_date,
                    release_date=first_air_date
                )
    
    return program
