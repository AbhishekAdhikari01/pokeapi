import requests
import re
from collections import defaultdict
from transformers import pipeline

# Initialize zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Universal definitions
ALL_ROLES = ["attacker", "tank", "support", "balanced", "special attacker", "physical attacker"]
ALL_TYPES = ["fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "fairy", 
             "fighting", "poison", "ground", "flying", "bug", "rock", "ghost", "steel", "normal"]

# Pokemon cache for performance
pokemon_cache = {}

def get_pokemon_info_cached(name):
    """Get Pokemon info with caching"""
    if name in pokemon_cache:
        return pokemon_cache[name]
    
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            pokemon_cache[name] = response.json()
            return pokemon_cache[name]
    except:
        pass
    return None

def determine_pokemon_role(pokemon_info):
    """Universal role determination based on stats"""
    if not pokemon_info:
        return "balanced"
    
    try:
        stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_info['stats']}
        
        hp = stats.get('hp', 0)
        attack = stats.get('attack', 0)
        defense = stats.get('defense', 0)
        sp_attack = stats.get('special-attack', 0)
        sp_defense = stats.get('special-defense', 0)
        speed = stats.get('speed', 0)
        
        # Advanced role calculation
        total_def = defense + sp_defense + hp
        total_att = attack + sp_attack
        
        # Tank: High defensive stats
        if (hp > 80 and defense > 70) or total_def > 220:
            return "tank"
        
        # Special Attacker: High sp_attack
        elif sp_attack > 90 or (sp_attack > attack and sp_attack > 70):
            return "special attacker"
        
        # Physical Attacker: High attack
        elif attack > 90 or (attack > sp_attack and attack > 70):
            return "physical attacker"
        
        # General Attacker: Good offensive stats with speed
        elif (total_att > 140 and speed > 60) or (attack > 65 and sp_attack > 65):
            return "attacker"
        
        # Support: High HP or balanced defensive stats
        elif hp > 75 or (defense + sp_defense > 120 and total_att < 140):
            return "support"
        
        else:
            return "balanced"
            
    except:
        return "balanced"

def universal_query_parser(text):
    """Universal parser for ANY query format"""
    text = text.lower().strip()
    print(f"Parsing query: '{text}'")
    
    requirements = defaultdict(int)
    
    # STEP 1: Handle numbers + roles/types patterns
    patterns = [
        r"(\d+)\s+(tank|tanks|attacker|attackers|support|supports|supporter|supporters|balanced|special\s*attacker|physical\s*attacker)",
        r"(\d+)\s+(fire|water|grass|electric|psychic|ice|dragon|dark|fairy|fighting|poison|ground|flying|bug|rock|ghost|steel|normal)\s*(type|types|pokemon|pokémon)?",
        r"(?:want|need|give\s*me|get\s*me)\s+(\d+)\s+(tank|tanks|attacker|attackers|support|supports|supporter|supporters|balanced|special\s*attacker|physical\s*attacker)",
        r"(?:want|need|give\s*me|get\s*me)\s+(\d+)\s+(fire|water|grass|electric|psychic|ice|dragon|dark|fairy|fighting|poison|ground|flying|bug|rock|ghost|steel|normal)",
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) >= 2:
                count = int(match[0])
                category = match[1].strip().replace('s', '').replace('er', '')  # normalize
                
                # Map to standard categories
                if category in ['tank']:
                    requirements['tank'] += count
                elif category in ['attack', 'attacker']:
                    requirements['attacker'] += count
                elif category in ['support', 'supporter']:
                    requirements['support'] += count
                elif category in ['balanced']:
                    requirements['balanced'] += count
                elif category in ['special attack', 'special attacker']:
                    requirements['special attacker'] += count
                elif category in ['physical attack', 'physical attacker']:
                    requirements['physical attacker'] += count
                elif category in ALL_TYPES:
                    requirements[category] += count
    
    # STEP 2: Handle specific Pokemon names
    pokemon_name_pattern = r"\b(pikachu|charizard|blastoise|venusaur|alakazam|gengar|dragonite|mewtwo|mew|articuno|zapdos|moltres)\b"
    pokemon_names = re.findall(pokemon_name_pattern, text)
    for name in pokemon_names:
        requirements[name] += 1
    
    # STEP 3: Handle general requests without numbers
    if not requirements:
        # Check for role mentions without numbers
        if any(word in text for word in ['tank', 'tanks']):
            requirements['tank'] = 6
        elif any(word in text for word in ['attack', 'attacker', 'attackers']):
            requirements['attacker'] = 6
        elif any(word in text for word in ['support', 'supporter', 'supporters']):
            requirements['support'] = 6
        elif any(word in text for word in ['balanced']):
            requirements['balanced'] = 6
        
        # Check for type mentions
        for poke_type in ALL_TYPES:
            if poke_type in text:
                requirements[poke_type] = 6
                break
    
    # STEP 4: Use NLP as fallback
    if not requirements:
        try:
            result = classifier(text, ALL_ROLES + ALL_TYPES)
            best_label = result['labels'][0] if result['scores'][0] > 0.3 else 'balanced'
            requirements[best_label] = 6
        except:
            requirements['balanced'] = 6
    
    print(f"Parsed requirements: {dict(requirements)}")
    return requirements

def get_all_pokemon_data():
    """Get all Pokemon data efficiently"""
    url = "https://pokeapi.co/api/v2/pokemon?limit=150"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get('results', [])
    except:
        pass
    return []

def build_team_universal(description, team_size=6):
    """Universal team builder for ANY query"""
    print(f"\n🔥 Building team for: '{description}'")
    
    # Parse requirements
    requirements = universal_query_parser(description)
    
    # Get Pokemon list
    all_pokemons = get_all_pokemon_data()
    if not all_pokemons:
        return []
    
    selected_team = []
    used_names = set()
    
    # PHASE 1: Fill specific requirements
    for requirement, needed_count in requirements.items():
        found_count = 0
        
        for pokemon_data in all_pokemons:
            if len(selected_team) >= team_size or found_count >= needed_count:
                break
                
            name = pokemon_data['name']
            if name in used_names:
                continue
            
            # Get Pokemon details
            info = get_pokemon_info_cached(name)
            if not info:
                continue
            
            # Extract Pokemon attributes
            p_types = [t['type']['name'] for t in info['types']]
            p_role = determine_pokemon_role(info)
            
            # Check if Pokemon matches requirement
            match = False
            
            if requirement == name:  # Specific Pokemon name
                match = True
            elif requirement in ALL_ROLES:  # Role requirement
                if requirement == p_role:
                    match = True
                elif requirement == 'attacker' and p_role in ['attacker', 'special attacker', 'physical attacker']:
                    match = True
            elif requirement in ALL_TYPES:  # Type requirement
                if requirement in p_types:
                    match = True
            
            if match:
                pokemon_obj = {
                    "name": name,
                    "types": p_types,
                    "role": p_role,
                    "stats": {stat['stat']['name']: stat['base_stat'] for stat in info['stats']}
                }
                selected_team.append(pokemon_obj)
                used_names.add(name)
                found_count += 1
                print(f"✅ Selected {name.title()} ({p_role}) for {requirement}")
    
    # PHASE 2: Fill remaining slots with balanced Pokemon
    while len(selected_team) < team_size:
        filled = False
        for pokemon_data in all_pokemons:
            if len(selected_team) >= team_size:
                break
                
            name = pokemon_data['name']
            if name in used_names:
                continue
            
            info = get_pokemon_info_cached(name)
            if not info:
                continue
            
            p_types = [t['type']['name'] for t in info['types']]
            p_role = determine_pokemon_role(info)
            
            pokemon_obj = {
                "name": name,
                "types": p_types,
                "role": p_role,
                "stats": {stat['stat']['name']: stat['base_stat'] for stat in info['stats']}
            }
            selected_team.append(pokemon_obj)
            used_names.add(name)
            filled = True
            break
        
        if not filled:  # Prevent infinite loop
            break
    
    return selected_team

def display_team_results(team, query):
    """Universal team display"""
    print(f"\n🎯 Final Team for: '{query}'")
    print(f"Team Size: {len(team)}")
    print("-" * 60)
    
    role_distribution = defaultdict(int)
    type_distribution = defaultdict(int)
    
    for i, pokemon in enumerate(team, 1):
        name = pokemon['name'].title()
        types = ' + '.join(pokemon['types']).title()
        role = pokemon['role'].title()
        
        print(f"{i}. {name:<12} | Types: {types:<20} | Role: {role}")
        
        role_distribution[pokemon['role']] += 1
        for ptype in pokemon['types']:
            type_distribution[ptype] += 1
    
    print(f"\n📊 Role Distribution: {dict(role_distribution)}")
    print(f"📊 Type Distribution: {dict(type_distribution)}")
    return role_distribution, type_distribution

# Main function to replace your build_team
def build_team(description, team_size=6):
    """Main function - replaces your existing build_team"""
    return build_team_universal(description, team_size)

# Testing function
def test_all_queries():
    """Test various query formats"""
    test_cases = [
        "i want 6 attackers",
        "4 tanks and 2 supporters", 
        "give me 3 fire type pokemon",
        "2 pikachu and 4 water types",
        "I need 1 special attacker 2 physical attackers 3 tanks",
        "6 balanced pokemon please",
        "mix of fire water and grass types",
        "strong attacking team",
        "defensive team with tanks",
        "3 electric 2 dragon 1 psychic"
    ]
    
    for query in test_cases:
        team = build_team_universal(query)
        display_team_results(team, query)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Example usage
    description = "i want 6 attackers"
    team = build_team(description)
    display_team_results(team, description)