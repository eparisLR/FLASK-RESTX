from os import stat
from flask import Flask, Response

from flask_restx import Resource, Api, reqparse
import random
import json
import os

from werkzeug.exceptions import BadHost, BadRequest

app = Flask(__name__)
api = Api(app)

#Cette route va permettre de retourner la valeur +1
@api.route('/plus_one/<int:number>')
@api.doc(params={"x": "Must be an integer."})
class Add(Resource):
    def get(self, number):
        return {'value': number+1}

#Cette route permet de retourner la valeur au carré et, pour mon cas j'ai testé de transmettre deux paramètres


@api.route('/square')
@api.doc(params={"int": "Must be an integer", "email": "Must be a string"}, location="query")
class Square(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('int', type=int)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        return {'value': args['int'] ** 2, 'email': args['email']}

#Cette route prend en paramètre le choix de l'utilisateur sous forme de int et renvoie le message final

@api.route('/game/<int:choice>')
@api.doc(params={"choice": "1: Pierre \n 2: Papier \n 3: Ciseaux \n 4: Lézard \n 5: Spock"})
class Game(Resource):
    def get(self, choice):
        liste_choices = ["Pierre", "Papier", "Ciseaux", "Lézard", "Spock"]

        def choice_computer(index):
            possibilities = ["Pierre", "Papier", "Ciseaux", "Lézard", "Spock"]
            possibilities.remove(possibilities[index])
            computer = possibilities[random.randint(0, len(possibilities)-1)]
            return computer
        
        if choice not in [1,2,3,4,5]:
            return Response(
        "Send a number between 1 and 5 !",
        status=400,
    )
        else: 
            user_choice= liste_choices[choice-1]
            computer_choice= choice_computer(choice-1)
            index_computer = liste_choices.index(computer_choice)

            result = {0: {1: True, 2: False, 3: True, 4: False },
            1: {0: True, 2: False, 3: False, 4: True}, 
            2: {0: False, 1: True, 3: True, 4: False}, 
            3: {0: False, 1: True, 2: False, 4: True}, 
            4: {0: True, 1: False, 2: True, 3: False} }

            if result[choice-1][index_computer] == False:
                with open('stats.json') as json_file:
                    data = json.load(json_file)
                    data[user_choice] = int(data[user_choice]) + 1
                    
                    with open('stats.json', 'w') as json_file:
                        json.dump(data, json_file)
                return {"ordinateur" : computer_choice, "user": user_choice, "message": "Vous avez perdu."}
            else:
                with open('stats.json') as json_file:
                    data = json.load(json_file)
                    data[user_choice] = int(data[user_choice]) + 1
                    
                    with open('stats.json', 'w') as json_file:
                        json.dump(data, json_file)
                    
                return {"ordinateur" : computer_choice, "user": user_choice, "message": "Vous avez gagné !"}

@api.route('/stats')
class Stats(Resource):
    def get(self):
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT,"stats.json")
        data = json.load(open(json_url))
        return data
    

if __name__ == '__main__':
    app.run(debug=True)