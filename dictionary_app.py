from flask import Flask,jsonify,abort,request,make_response
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)


app.config.update({
   "DEBUG": True
})

users = [
    {
        'username': 'dhannu','password': 'p'
    }
]

words = [
    {
        'word': 'counter',
        'note': 'counter ka matlab hota hain count karne wala',
        'username': 'dhannu',
        'difficult': "3",
        'id': 7
    },

    {
        'word': 'apple',
        'note': 'apple ka matlab hota hain seb jisse ham khate hain',
        'username': 'dhannu',
        'difficult': "2",
        'id': 3
    },
    {
        'word': 'something',
        'note': 'something means, kuch',
        'username': 'dhannu',
        'difficult': "6",
        'id': 4
    },
        {
        'word': 'fast',
        'note': 'fast means, jo tej hota hain',
        'username': 'dhannu',
        'difficult': "5",
        'id': 1
    }
]

@auth.get_password
def get_passwords(username):
    new = [user for user in users if username == user['username']]
    if len(new) == 0:
        abort(404)
    return new[0]['password']

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)



@app.route('/add', methods = ['GET'])
@auth.login_required
def add_name():
    new_word = [word for word in words if auth.username() == word['username']]
    user = request.args.get('user')
    if user == 'id':
        new_word = sorted(new_word, key=lambda k: k['id'])
    if user == 'word':
        new_word = sorted(new_word, key=lambda k: k['word'])
    if user == 'difficult':
        new_word = sorted(new_word, key=lambda k: k['difficult'])
    return jsonify({'username': new_word})

@app.route('/add/add_user', methods = ['POST'])
def adding():
    if not request.json or not 'username' in request.json:
        abort(400)
    add = {
        'username': request.json['username'],
        'password': request.json['password']
    }
    users.append(add)
    return jsonify({'userss': add}), 201

@app.route('/add/add_user/more_word', methods = ['POST'])
def more_words():
    if not request.json or not 'word' in request.json:
        abort(400)
    add_new_words = {
        'id': words[-1]['id'] +1,
        'username': auth.username(),
        'word': request.json['word'],
        'note': request.json['note'],
        'difficult': request.json['difficult']
    }

    words.append(add_new_words)
    return jsonify({'words': add_new_words}), 201

if __name__ == '__main__':
   app.run()
