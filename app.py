from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import json

# Config
DEBUG = True

# Instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)


THEORIES = []
PLAYERS = []

# Sanity Checks
@app.route('/ping', methods=['GET'])
def pingPong():
    return jsonify('pong')

@app.route('/Theories', methods=['GET', 'POST'])
def all_Theories():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        add_Theory(post_data.get('title'),
                 post_data.get('author'),
                 post_data.get('proposedTheory'),
                 post_data.get('bets'),
                 uuid.uuid1().hex)
        response_object['message'] = 'Theory added!'
    else:
        response_object['Theories'] = THEORIES
    return jsonify(response_object)

@app.route('/players', methods=['GET'])
def all_players():
    response_object = {'status': 'success'}
    response_object['players'] = PLAYERS
    return jsonify(response_object)


@app.route('/Theories/<Theory_id>', methods=['PUT', 'DELETE'])
def single_Theory(Theory_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        #To update a record we delete it and add it again
        post_data = request.get_json()
        if(remove_Theory(Theory_id)):
            add_Theory(post_data.get('title'),
                     post_data.get('author'),
                     post_data.get('proposedTheory'),
                     post_data.get('bets'),
                     Theory_id)
            response_object['message'] = 'Theory updated!'
        else:
            response_object['status'] = 'Fail'
    if request.method == 'DELETE':
        if(remove_Theory(Theory_id)):
            response_object['message'] = 'Theory updated!'
        else:
            response_object['status'] = 'Fail'
    return jsonify(response_object)

def add_Theory(TheoryTitle, TheoryAuthor, theoryContent, TheoryBets, uniqueID):
    global THEORIES
    betPos, betNeg = individualVoteCalc(TheoryBets)
    THEORIES.append({
        'id': uniqueID,
        'title': TheoryTitle,
        'author': TheoryAuthor,
        'proposedTheory': theoryContent,
        'bets': TheoryBets,
        'positive': betPos,
        'negative': betNeg
    })
    update_local()

@app.route('/players/<player_id>', methods=['PUT'])
def single_player(player_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    if(remove_Theory(Theory_id)):
        add_Theory(post_data.get('name'),
                 post_data.get('tokensTotal'),
                 post_data.get('bets'),
                 Theory_id)
        response_object['message'] = 'Player modified!'
    else:
        response_object['status'] = 'Fail'
    return jsonify(response_object)

def remove_Theory(Theory_id):
    for Theory in THEORIES:
        if Theory['id'] == Theory_id:
            THEORIES.remove(Theory)
            update_local()
            return True
    return False

def remove_player(player_id):
    for player in PLAYERS:
        if player['id'] == player_id:
            PLAYERS.remove(player)
            update_local()
            return True
    return False

def add_player(authorName, tokensTotal, bets, uniqueID = uuid.uuid4().hex):
    global PLAYERS
    PLAYERS.append({
        'id': uniqueID,
        'name': authorName,
        'tokensTotal': tokensTotal,
        'bets': bets
    })

def individualVoteCalc(voteBets):
    countPos = 0
    countNeg = 0
    for bet in voteBets: 
        if bet["betAmount"] > 0:
            countPos += bet["betAmount"]
        else:
            countNeg += abs(bet["betAmount"])
    return (countPos, countNeg)

# JSON helpers
def load_Theories():
    global THEORIES
    with open('Theories.json') as infile:
        THEORIES = json.load(infile)

def load_players():
    global PLAYERS
    with open('players.json') as infile:
        PLAYERS = json.load(infile)

def update_local():
    global THEORIES
    with open('Theories.json', 'w') as outfile:
        json.dump(THEORIES,outfile)

def update_players():
    global PLAYERS
    with open('players.json', 'w') as outfile:
        json.dump(PLAYERS,outfile)

# Core
if __name__ == '__main__':
    load_Theories()
    load_players()
    app.run()
