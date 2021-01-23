import flask
from flask import request, jsonify
from flask_restful import Api, Resource
import json
import random



app = flask.Flask(__name__)
api = Api(app)

app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Vulnerable Rest API</h1><p>Please find /api/ path.</p>"

def append_data_to_make_final_userfile(users_data):
    with open('users.json', 'r') as f:
        json_data = json.load(f)
        json_data.append(users_data)
        new_json = json.dumps(json_data)
        return new_json


@app.route('/api/v1/users/create', methods=['POST'])
def postrequest():  
    # id = random.randint(1111,9999)
    req_data = request.get_json()
    
    # req_data['id'] = id    
    final_data = append_data_to_make_final_userfile(req_data)
    print (final_data)
    with open('users.json', 'w') as f:
        f.write(str(final_data))
    return 'Success'

def getdata():

    with open('users.json', 'r') as f:
        json_data = json.load(f)
        return json_data


        # how can we convert single quote to double quote, here when using json.dumps it returns

class users(Resource):
    def get(self, id):
        data = getdata()
        for sets in data:
            print (sets)
            if id == str(sets['id']):
                return jsonify(sets)

    def delete(self, id):
        data = getdata()
        for sets in data:
            if id == sets['id']:
                print('id Found - Deleting as we receive DELETE method', id)
                del sets['id']
                return None

api.add_resource(users, '/api/v1/users/<string:id>')
app.run()