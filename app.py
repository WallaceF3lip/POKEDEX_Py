from flask import Flask, jsonify, render_template
from flask.globals import request
import requests
import json

from models.pokemon import Pokemon

app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("index.html", 
                        name = '...', 
                        picture = 'static\images\pikachu-silhueta.png',
                        )

all = json.loads(requests.get('https://pokeapi.co/api/v2/pokemon?limit=2000&offset=0').text)
AllPokemons = []
for i in range(len(all['results'])):
    AllPokemons.append(all['results'][i]['name'])


@app.route('/search_like', methods=['GET'])
def search_like():
    termo = request.args.get('termo')  # Obter o termo de pesquisa da query string
    resultados = [dado for dado in AllPokemons if termo.lower() in dado.lower()]
    return jsonify(resultados)


@app.route("/search", methods=["GET", "post"])
def search():
    pokemon = Pokemon(request.form['name_pokemon'].lower(),'','','','')
    try:
        res = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.name}").text)
        
        pokemon.picture = res['sprites']['front_default']

        pokemon.type1 = res['types'][0]['type']['name']
        if len(res['types']) > 1:
            pokemon.type2 = res['types'][1]['type']['name']
        
        pokemon.moves = []
        for i in range(len(res['moves'])):
            pokemon.moves.append(res['moves'][i]['move']['name'])

    except: 
        return render_template("index.html", 
                        name = '...', 
                        picture = 'static\images\pikachu-silhueta.png', 
                        type1 = pokemon.type1.upper(), 
                        type2 = pokemon.type2.upper(),
                        moves = pokemon.moves,
                        toast = True
                        )
    
    return render_template("index.html", 
                        name = pokemon.name, 
                        picture = pokemon.picture, 
                        type1 = pokemon.type1.upper(), 
                        type2 = pokemon.type2.upper(),
                        moves = pokemon.moves,
                        toast = False
                        )


if __name__ == "__main__":
    app.run(debug=True)