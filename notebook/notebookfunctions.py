from .models import Provider, Program
import requests
import json
import os

API_KEY = os.environ.get("TMDB_TOKEN", "test")

# Function to create program in one click
def getProgramData(tmdb_id, media_type):

    params = dict(api_key=API_KEY, language="fr-FR")

    if media_type == "tv":
        req = requests.get("https://api.themoviedb.org/3/tv/{}".format(tmdb_id), params)

        if req.status_code != 200:
            return False, None  # Raise an error or write log here

        try:
            data = json.loads(req.content)

            origins = [network["origin_country"] for network in data["networks"]]
            list_networks = [network["name"] for network in data["networks"]]

            name = data["name"]
            original_name = data["original_name"]
            last_air_date = data["last_air_date"]
            first_air_date = data["first_air_date"]
            program_format = 1

        except KeyError:
            return False, None  # Write specific message here in logs

        except json.JSONDecodeError as jsonErr:
            return False, None  # Write specific message here in logs

    elif media_type == "movie":
        req = requests.get(
            "https://api.themoviedb.org/3/movie/{}".format(tmdb_id), params
        )

        if req.status_code != 200:
            return False, None  # Raise an error or write log here

        try:
            data = json.loads(req.content)

            origins = [
                production_company["name"]
                for production_company in data["production_countries"]
            ]
            list_networks = [
                production_company["name"]
                for production_company in data["production_companies"]
            ]

            name = data["title"]
            original_name = data["original_title"]
            last_air_date = data["release_date"]
            first_air_date = data["release_date"]
            program_format = 0

        except KeyError:
            return False, None  # Write specific message here in logs

        except json.JSONDecodeError as jsonErr:
            return False, None  # Write specific message here in logs

    else:

        return False, None  # Raise an error or write log here

    list_genres = [genre["name"] for genre in data["genres"]]

    program = dict(
        tmdb_id=tmdb_id,
        name=name,
        format=program_format,
        homepage_link=data["homepage"],
        source=", ".join(list_networks),
        origin_country=", ".join(origins),
        original_name=original_name,
        synopsis=data["overview"],
        poster_path=data["poster_path"],
        tags=", ".join(list_genres),
        last_air_date=last_air_date,
        release_date=first_air_date,
    )

    return program


def getProviders(tmdb_id, media_type):

    list_providers = []

    params = dict(api_key=API_KEY, language="fr-FR")
    req = requests.get(
        f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}/watch/providers", params
    )

    if req.status_code != 200:
        raise KeyError

    try:
        data_providers = json.loads(req.content)

        for key in data_providers["results"]["FR"].keys():
            if key == "link":
                link = data_providers["results"]["FR"][key]

            else:
                for req_provider in data_providers["results"]["FR"][key]:

                    provider = dict(
                        provider_name=req_provider["provider_name"],
                        provider_tmdb_id=req_provider["provider_id"],
                        logo_url=req_provider["logo_path"],
                    )

                    new_provider, created = Provider.objects.get_or_create(
                        provider_tmdb_id=req_provider["provider_id"], defaults=provider
                    )

                    list_providers.append(new_provider)

    except KeyError:
        return False, None
        # return False  # Write specific message here in logs

    except json.JSONDecodeError as jsonErr:
        return False, None
        # return False # Write specific message here in logs

    return list_providers, link


"""
Method to get programs similars programs
"""


def addSimilarPrograms(program):

    media_type = "tv" if program.format == 1 else "movie"

    try:
        params = dict(
            api_key=API_KEY, language="fr-FR", page=1
        )
        req_reco = requests.get(
            f"https://api.themoviedb.org/3/{media_type}/{program.tmdb_id}/recommendations",
            params,
        )
        if req_reco.status_code == 200:
            data_reco = json.loads(req_reco.content)
        else:
            # print(f"Status code : {req_reco.status_code}")
            raise KeyError
    except KeyError:
        pass

    for program in data_reco["results"][:15]:
        similar_program_querry = Program.objects.filter(tmdb_id=program.id)
        for similar_program in similar_program_querry:
            program.similars.add(similar_program)

    return True
