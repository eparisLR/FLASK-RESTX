from flask import Flask
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

@api.route('/plus_one/<int:number>')
class Add(Resource):
    def get(self, number):
        return {'value': number+1}

@api.route('/square')
class Square(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('int', type=int)
        args = parser.parse_args()
        return {'value' : args['int'] ** 2}

if __name__ == '__main__':
    app.run(debug=True)