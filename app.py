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


BOOKS = []
PLAYERS = []

# Sanity Checks
@app.route('/ping', methods=['GET'])
def pingPong():
    return jsonify('pong')

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        add_book(post_data.get('title'),
                 post_data.get('author'),
                 post_data.get('theory'))
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/players', methods=['GET'])
def all_players():
    response_object = {'status': 'success'}
    response_object['players'] = PLAYERS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        if(remove_book(book_id)):
            add_book(post_data.get('title'),
                     post_data.get('author'),
                     post_data.get('read'),
                     book_id)
            response_object['message'] = 'Book updated!'
        else:
            response_object['status'] = 'Fail'
    if request.method == 'DELETE':
        if(remove_book(book_id)):
            response_object['message'] = 'Book updated!'
        else:
            response_object['status'] = 'Fail'
    return jsonify(response_object)

def add_book(bookTitle, bookAuthor, bookRead, uniqueID = uuid.uuid4().hex):
    global BOOKS
    BOOKS.append({
        'id': uniqueID,
        'title': bookTitle,
        'author': bookAuthor,
        'read': bookRead
    })
    update_local()

@app.route('/players/<player_id>', methods=['PUT'])
def single_player(player_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    if(remove_book(book_id)):
        add_book(post_data.get('name'),
                 post_data.get('tokensTotal'),
                 post_data.get('bets'),
                 book_id)
        response_object['message'] = 'Player modified!'
    else:
        response_object['status'] = 'Fail'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
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

def load_books():
    global BOOKS
    with open('books.json') as infile:
        BOOKS = json.load(infile)

def load_players():
    global PLAYERS
    with open('players.json') as infile:
        PLAYERS = json.load(infile)

def update_local():
    global BOOKS
    with open('books.json', 'w') as outfile:
        json.dump(BOOKS,outfile)

def update_players():
    global PLAYERS
    with open('players.json', 'w') as outfile:
        json.dump(PLAYERS,outfile)

# Core
if __name__ == '__main__':
    load_books()
    load_players()
    app.run()
