import json 
from myExceptions import *
from flask import Flask, request ## Importing Flask Class
from flask_expects_json import expects_json
app = Flask(__name__) ## Creating new instance of Flask class


# List all users
@app.route('/')
def hello():
    with open('users.json') as users_file:
        data = json.load(users_file)
    return data

# Get user with specific user id
@app.route('/<id>')
def getUser(id):
    try:
        id = int(id)
        data = dict()
        with open('users.json') as users_file:
            users = json.load(users_file)
            for user in users:
                if int(user['id']) == int(id):
                    data.update(user)
                    return({
                    'status': 200,
                    'body':data
                    })

            if not bool(data):
                raise ValueNotFound


    except ValueNotFound:
          return({
            'status': 404,
            'error': 'Not Found',
            'message':'No record found for given id'
            })
    except ValueError:
        return({
            'status': 400,
            'error': 'Bad Request',
            'message':'Please input integer value as id'
            })
    

@app.route('/delete/<id>')
def deleteUser(id):
    try:
        id = int(id)
        data = dict()
        with open('users.json') as users_file:
            users = json.load(users_file)
            for user in users:
                if user['id'] == id:
                    # print('//////////')
                    # print(users.index(user))
                    # data1 = users.pop(users.index(user))

                    users.remove(user)

                    return ({
                    'status':200,
                    'message':'Deletion Successful',
                    'data deleted':  user
                    })

            if not bool(data):
                raise ValueNotFound('Detail Not Found')


    except ValueNotFound as e:
          return({
            'status': 404,
            'error': str(e),
            'message':'No record found for given id'
            })
    except ValueError:
        return({
            'status': 400,
            'error': 'Bad Request',
            'message':'Please input integer value as id'
            })

# defines content of the json file
schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "number"},
                "geo": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"}
                    }
                }
            }
        },
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs": {"type": "string"}
            }
        }
    }
}

# update
@app.route('/update/<id>',methods='POST')
def updateUser(id):
    body = request.json()
    try:
        id = int(id)
        data = dict()
        with open('users.json') as users_file:
            users = json.load(users_file)
        for user in users:
            if user['id'] == id:
                for key,item in body:
                    user[key] = item
        with open('users.json', 'w') as users_file_write:
            json.dump(users, users_file_write)
        if not bool(data):
            raise ValueNotFound('Detail Not Found')
        response = {
            'status': 200,
            'message': 'User updated successfully',
            "data": body
        }
    except ValueNotFound as e:
          return({
            'status': 404,
            'error': str(e),
            'message':'No record found for given id'
            })
    except ValueError:
        return({
            'status': 400,
            'error': 'Bad Request',
            'message':'Please input integer value as id'
            })

    return response

@app.route('/users/create/',methods=['POST'])
@expects_json(schema)
def addUser():
    body = request.get_json()
    with open('users.json') as users_file:
        users = json.load(users_file)
    users.append(body)
    with open('users.json', 'w') as users_file_write:
        json.dump(users, users_file_write)

    response = {
        'status':200,
        'message':'User Added Successfully',
        'user':  body
    }
    return response

