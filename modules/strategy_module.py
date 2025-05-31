# modules/strategy_module.py
from .info_module import get_pokemon_info

# Module-level type advantages chart
type_advantages = {
    "normal": [],
    "fire": ["grass", "ice", "bug", "steel"],
    "water": ["fire", "ground", "rock"],
    "electric": ["water", "flying"],
    "grass": ["water", "ground", "rock"],
    "ice": ["grass", "ground", "flying", "dragon"],
    "fighting": ["normal", "ice", "rock", "dark", "steel"],
    "poison": ["grass", "fairy"],
    "ground": ["fire", "electric", "poison", "rock", "steel"],
    "flying": ["grass", "fighting", "bug"],
    "psychic": ["fighting", "poison"],
    "bug": ["grass", "psychic", "dark"],
    "rock": ["fire", "ice", "flying", "bug"],
    "ghost": ["psychic", "ghost"],
    "dragon": ["dragon"],
    "dark": ["psychic", "ghost"],
    "steel": ["ice", "rock", "fairy"],
    "fairy": ["fighting", "dragon", "dark"]
}

def get_type_advantage(type1, type2):
    """
    Simplified single-type advantage:
    +1 if type1 strong vs type2,
    -1 if type1 weak vs type2,
     0 otherwise.
    """
    # strong
    if type2 in type_advantages.get(type1, []):
        return 1
    # weak (i.e. type2 is strong vs type1)
    if type1 in type_advantages.get(type2, []):
        return -1
    return 0

def calculate_type_advantages(attacker_types, defender_types):
    """
    Compare lists of attacker_types vs defender_types.
    Sum up +1/-1 for each type matchup.
    Returns integer score; higher means attacker has advantage.
    """
    score = 0
    for atk_type in attacker_types:
        for def_type in defender_types:
            score += get_type_advantage(atk_type, def_type)
    return score

def suggest_counter_types(opponent_types):
    counter_types = set()
    for opp_type in opponent_types:
        for type_name, strong_against in type_advantages.items():
            if opp_type in strong_against:
                counter_types.add(type_name)
    return list(counter_types)


def strategy_decision(pokemon1_name, pokemon2_name):
    """
    Full strategy decision given two Pokémon names.
    Fetches their types via get_pokemon_info, then compares.
    """
    p1 = get_pokemon_info(pokemon1_name)
    p2 = get_pokemon_info(pokemon2_name)

    if 'error' in p1 or 'error' in p2:
        return {"error": "One or both Pokémon not found."}

    score1 = calculate_type_advantages(p1["types"], p2["types"])
    score2 = calculate_type_advantages(p2["types"], p1["types"])

    if score1 > score2:
        winner = p1['name']
        loser_types = p2['types']
        counter_suggestions = suggest_counter_types(loser_types)
    elif score2 > score1:
       winner = p2['types']
       loser_types = p1['types']
       counter_suggestions = suggest_counter_types(loser_types)
    else:
       winner = 'Tie'
       counter_suggestions = []
    

    return{
        "winner": winner,
        "pokemon1_types": p1["types"],
        "pokemon2_types": p2["types"],
        "score1": score1,
        "score2": score2,
        "suggested_counters": counter_suggestions

    }

# Testing block
if __name__ == "__main__":
    print(strategy_decision("pikachu", "charizard"))
