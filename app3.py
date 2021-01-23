import hashlib
import uuid
import flask
from flask import request, jsonify
from flask_restful import Api, Resource
import json
import random
import base64
from functools import wraps


app = flask.Flask(__name__)
api = Api(app)

app.config["DEBUG"] = True
username='admin'
password='admin12221'

@app.route('/token', methods=['GET'])
def tokengeneration():
    tokenform = username+':'+password
    encode_base64 = base64.b64encode(tokenform.encode())
    return encode_base64

@app.route('/', methods=['GET'])
def home():
    return "<h1>Vulnerable Rest API</h1><p>Please find /api/ path.</p>"



# hashid = hash_uid(id)
# print (check_id(hashid, 1))

def append_data_to_make_final_userfile(users_data):
    with open('users2.json', 'r') as f:
        json_data = json.load(f)
        json_data.append(users_data)

        new_json = json.dumps(json_data)
        return new_json
  
def getdata():

    with open('users2.json', 'r') as f:
        json_data = json.load(f)
        return json_data
        # how can we convert single quote to double quote, here when using json.dumps it returns

salt = uuid.uuid4().hex
def hash_uid(id):
    
    return hashlib.sha256(salt.encode() + str(id).encode()).hexdigest()

def hash_id_return_salt(id):
    return hashlib.sha256(salt.encode() + str(id).encode()).hexdigest() + ':' + salt

def check_id(hashid, user_provided_id):
    password, salt = hash_id_return_salt.split(':')
    return password == hashlib.sha256(salt.encode()+str(user_provided_id).encode()).hexdigest()

@app.route('/api/v1/users/create', methods=['POST'])
def postrequest():  
    id = random.randint(1111, 9999)
    req_data = request.get_json()
    req_data['id'] = hash_uid(id)  
    final_data = append_data_to_make_final_userfile(req_data)
    with open('users2.json', 'w') as f:
        f.write(str(final_data))
    return 'Success'

def check_token(token):
    
    if str(token) == str(tokengeneration().decode()):
        return True

def requires_auth(f):
    @wraps(f)
    def checker(*args, **kwargs):
        print ('aaaa')
        if not check_token(request.headers['Authorization']):
            error = "Please provide valid token"
            return error, 401
        return f(*args, **kwargs)
    return checker

class users(Resource):
    @requires_auth
    def get(self, id):        
        data = getdata()
        for sets in data:
            if id == sets['id']:
                return jsonify(sets)
        

    def delete(self, id):
        data = getdata()
        
        newdata = []
        for sets in data:
            if id == sets['id']:
                print('id Found - Deleting as we receive DELETE method', id)
                del sets
            else:
                newdata.append(sets)

        print (newdata)
        with open('users2.json', 'w') as f:
            data2 = json.dumps (newdata)
            f.write(str(data2))
            return 'Success'


api.add_resource(users, '/api/v1/users/<string:id>')
app.run()