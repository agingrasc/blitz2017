import json
from flask import abort, Flask, jsonify, make_response, request

import feed

app = Flask("Natural 20")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/")
def index():
    return jsonify({'message': "Bienvenu sur le serveur d'authentification de Natural 20"})

@app.route("/subscribe", methods=['POST'])
def subscribe():
    global team_info

    _validate_request(request)
    nbrItems = request.json['numberOfItems']
    calories = request.json['calories']
    items = feed.find_meal(calories, nbrItems)
    team_info['answer'] = items
    return jsonify(team_info)


def _validate_request(request):
    if not request.json:
        print('not in json')
        abort(400)
    if not 'numberOfItems' in request.json:
        print('no field "numberOfItems"')
        abort(400)
    if not 'calories' in request.json:
        print('no field "calories"')
        abort(400)
    if not 'menuUrl' in request.json:
        print('no field "menuUrl"')
        abort(400)

def _get_team_info():
    """ Retourne les informations de l'equipe """
    equipe_as_json = ""
    with open('../data/equipe.json') as equipe_file:
        for line in equipe_file.readlines():
            equipe_as_json += line

    return json.loads(equipe_as_json)

if __name__ == "__main__":
    team_info = _get_team_info()
    app.run()
