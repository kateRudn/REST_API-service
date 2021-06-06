import json
from app import app
from flask import jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from app import db, database
import requests
import hashlib

auth = HTTPBasicAuth()

@auth.verify_password
def verifyPassword(username, password):
    user = database.User.query.filter_by(userName=username).first()
    if not user: abort(401)
    return username == user.userName and hash(password) == user.userPassword

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def correctUser(username):
    users = database.User.query.all()
    strUsers = [str(item) for item in users]
    if username not in strUsers: return 1
    return 0

def hash(password):
    hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return str(hashPassword)

@app.route('/registration', methods=['GET']) #
@auth.login_required
def createUser():
    authData = request.authorization
    username = authData['username']
    password = authData['password']
    hashPassword = hash(password)
    if not correctUser(username):
        return jsonify({'Error': 'user is in database'})
    u = database.User(userName=username, userPassword=hashPassword)
    db.session.add(u)
    db.session.commit()
    return jsonify({'Username': username})

@app.route('/jokes', methods=['GET']) # get all jokes for user
@auth.login_required
def getJokes():
    authData = request.authorization
    username = authData['username']
    jokes = database.Jokes.query.filter_by(userName=username)
    result = []
    for j in jokes:
        result.append({'id': str(j.idJoke),
                       'joke': str(j.contentJoke)})
    # d = json.dumps(result)
    return str(result)

@app.route('/jokes/<int:id>', methods=['GET']) # get joke for user by id
@auth.login_required
def getJoke(id):
    authData = request.authorization
    username = authData['username']
    joke = database.Jokes.query.filter_by(userName=username, idJoke=id).first()
    if not joke: return jsonify({'Error': 'no joke with that name'})
    return jsonify({'Joke': joke.contentJoke})

@app.route('/jokes/create', methods=['POST']) # create joke for user
@auth.login_required
def createJoke():
    if not request.json or not 'joke' in request.json:
        abort(400)
    newJoke = request.json['joke']
    authData = request.authorization
    username = authData['username']
    user = database.User.query.filter_by(userName=username).first()
    joke = database.Jokes(contentJoke=newJoke, author=user)
    db.session.add(joke)
    db.session.commit()
    return jsonify({username: newJoke})

@app.route('/jokes/generate', methods=['POST']) # generate joke for user
@auth.login_required
def generateJoke():
    authData = request.authorization
    username = authData['username']
    response = requests.get('https://geek-jokes.sameerkumar.website/api')
    newJoke = response.json()
    user = database.User.query.filter_by(userName=username).first()
    joke = database.Jokes(contentJoke=newJoke, author=user)
    db.session.add(joke)
    db.session.commit()
    return jsonify({username: newJoke})

@app.route('/jokes/<int:id>', methods=['PUT']) # update joke for user by id
@auth.login_required
def updateJoke(id):
    if not request.json or not 'joke' in request.json:
        abort(400)
    newJoke = request.json['joke']
    authData = request.authorization
    username = authData['username']
    joke = database.Jokes.query.filter_by(userName=username, idJoke=id).first()
    if not joke: return jsonify({'Error': 'no joke with that name'})
    joke = database.Jokes.query.filter_by(userName=username, idJoke=id).first()
    joke.contentJoke=newJoke
    db.session.commit()
    return jsonify({'Joke': newJoke})

@app.route('/jokes/<int:id>', methods=['DELETE']) # delete joke for user by id
@auth.login_required
def deleteJoke(id):
    authData = request.authorization
    username = authData['username']
    joke = database.Jokes.query.filter_by(userName=username, idJoke=id).first()
    if not joke: return jsonify({'Error': 'no joke with that name'})
    db.session.delete(joke)
    db.session.commit()
    return jsonify({'result': True})