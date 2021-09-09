from flask import Flask
from flask_restx import Resource, Api, reqparse
import random

app = Flask(__name__)
api = Api(app)

@api.route('/plus_one/<int:number>')
@api.doc(params={"x": "Must be an integer."})
class Add(Resource):
    def get(self, number):
        return {'value': number+1}

@api.route('/square')
class Square(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('int', type=int)
        args = parser.parse_args()
        return {'value': args['int'] ** 2}

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
            return {"message": "Veuillez entrer un nombre entre 1 et 5 !"}
        else: 
            user_choice= liste_choices[choice]
            computer_choice= choice_computer(choice)
            index_computer = liste_choices.index(computer_choice)

            result = {0: {1: True, 2: False, 3: True, 4: False },
            1: {0: True, 2: False, 3: False, 4: True}, 
            2: {0: False, 1: True, 3: True, 4: False}, 
            3: {0: False, 1: True, 2: False, 4: True}, 
            4: {0: True, 1: False, 2: True, 3: False} }

            if result[choice][index_computer] == False:
                return {"message": f"Vous avez joué : {user_choice} et, l'ordinateur a joué : {computer_choice}. Vous avez perdu."}
            else:
                return {"message": f"Vous avez joué : {user_choice} et, l'ordinateur a joué : {computer_choice}. Vous avez gagné !"}

if __name__ == '__main__':
    app.run(debug=True)