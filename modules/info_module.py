import requests
import logging

# Logging setup

logger = logging.getLogger(__name__)
 
def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()


        info = {
            "name": data["name"],
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "base_experience": data["base_experience"],
            "stats": data["stats"],
             
         }

        logger.info(f"Fetched info for{pokemon_name}")
        return info
    
    except requests.exceptions.RequestsException as e:
        logger.error(f"Error fetching info for {pokemon_name}: {e}")
        return {"error": f"Could not fetch info for {pokemon_name}"}
    