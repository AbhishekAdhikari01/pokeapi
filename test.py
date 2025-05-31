##from modules.info_module import get_pokemon_info

#if __name__ == "__main__":
  #  result = get_pokemon_info("pikachu")
   # print(result)


#from modules.compare_module import compare_pokemons

#if __name__ == "__main__":
    #pokemon1 = "pikachu"
    #pokemon2 = "pikachu"
    
    #result = compare_pokemons(pokemon1, pokemon2)
    #print("Comparison result:")
    #print(result)





#from modules.strategy_module import strategy_decision
#print(strategy_decision("pikachu", "charizard"))
##print(strategy_decision("pikachu","garchomp"))
#print(strategy_decision("flygon","garchomp"))





from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()