from flask import Flask, request, jsonify
import logging
import requests
from flask_cors import CORS
from modules.info_module import get_pokemon_info
from modules.compare_module import compare_pokemons
from modules.strategy_module import strategy_decision
from modules.team_module import build_team

# Setup Logging
logging.basicConfig(
    filename='mcp.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Also log to console (optional)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# -- Routes --

@app.route('/info', methods=['POST'])
def info():
    data = request.get_json()  # ✅ FIXED: request (not requests)
    name = data.get('name')
    
    logging.info(f"/info called with: {name}")
    
    if not name:
        logging.warning("No Pokemon name provided in /info")
        return jsonify({'error': 'Please provide a pokemon name'}), 400
    
    result = get_pokemon_info(name)
    return jsonify(result)

@app.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()  # ✅ FIXED: request (not requests)
    p1 = data.get('pokemon1')
    p2 = data.get('pokemon2')
    
    logging.info(f"/compare called with: {p1} vs {p2}")
    
    if not p1 or not p2:
        logging.warning("Missing one or both Pokemon names in /compare")
        return jsonify({'error': 'Please provide both Pokemon names'}), 400
    
    result = compare_pokemons(p1, p2)
    return jsonify(result)

@app.route('/strategy', methods=['POST'])
def strategy():
    data = request.get_json()  # ✅ FIXED: request (not requests)
    name1 = data.get('name1')
    name2 = data.get('name2')
    
    logging.info(f"/strategy called with: {name1}")
    
    if (not name1) or (not name2):
        logging.warning("No Pokemon name provided in /strategy")
        return jsonify({'error': 'Please provide a Pokemon name'}), 400
    
    result = strategy_decision(name1,name2)
    return jsonify(result)

@app.route('/team', methods=['POST'])
def team():
    data = request.get_json()  # ✅ FIXED: request (not requests)
    description = data.get('description', '')
    
    logging.info(f"/team called with description: {description}")
    
    if not description:
        logging.warning("No description provided in /team")
        return jsonify({'error': 'Please provide a team description'}), 400
    
    team = build_team(description, team_size=6)
    return jsonify(team)

# -- Run Server --

if __name__ == "__main__":
    logging.info("Starting MCP server...")
    app.run(debug=True)