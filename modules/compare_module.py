from modules.info_module import get_pokemon_info
def get_stat_value(stats , stat_name):
    for stat in stats:
        if stat['stat']['name'] == stat_name:
            return stat['base_stat']
    return 0

def compare_pokemons(pokemon1_name , pokemon2_name):
    p1 = get_pokemon_info(pokemon1_name)
    p2 = get_pokemon_info(pokemon2_name)


    if  not p1 or not p2:
        return "One or both pokemon not found" 
    
    comparison = {
        "name": [p1["name"], p2["name"]],
        "height": [p1["height"], p2["height"]],
        "weight":[p1["weight"] ,p2["weight"]],
        "types":[p1["types"], p2["types"]],
        "abilities": [p1["abilities"],p2["abilities"]],
        "base_experience": [p1["base_experience"], p2["base_experience"]],
        "stats": [p1["stats"], p2["stats"]],
    }

    #Simple Comparision result

    p1_point = 0
    p2_point = 0
    stats_winner = {}

    # Compare height
    
    if p1['height'] > p2["height"]:
        height_winner = p1["name"]
        p1_point += 1
    elif p2["height"] > p1["height"]:
        height_winner = p2["name"]
        p2_point += 1
    else :
        height_winner = "Tie"
    

    # Compare weight

    if p1['weight'] > p2["weight"]:
        weight_winner = p1["name"]
        p1_point += 1
    elif p2["weight"] > p1["weight"]:
        weight_winner = p2["name"]
        p2_point += 1
    else :
        weight_winner = "Tie"  

     ## stats compare

    stats_to_compare = ["hp","attack","defence","special-attack","speed"]

    for stat in stats_to_compare:
        p1_value = get_stat_value(p1["stats"],stat)
        p2_value = get_stat_value(p2["stats"],stat)
          

        if p1_value > p2_value:
            winner = p1["name"]
            p1_point += 1
        elif p2_value > p1_value:
            winner = p2["name"]
            p2_point += 1
        else:
            winner = "Tie"
        stats_winner[stat] = {
            p1["name"]: p1_value,
            p2["name"]: p2_value,
            "winner": winner

        }

    ## overall winner based on total points

    if p1_point > p2_point:
        overall_winner = p1['name']
    elif p2_point > p1_point:
        overall_winner = p2['name']
    else:
        overall_winner = "Tie"


    comparison["height_winner"] = height_winner    
    comparison["weight_winner"] = weight_winner  
    comparison["overall_winner"] = overall_winner    
    
    return comparison


if __name__ == "__main__":
    result = compare_pokemons("pikachu" ,"charizard")
    print(result)