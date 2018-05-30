
# -- coding: utf-8 --
from flask import Flask
from flask import jsonify
from flask_cors import *
from flask import request
app = Flask(__name__)
CORS(app, supports_credentials=True)



@app.route('/')
def index():
    type1 = {
        'title':'首页',
        'b': 2,
        'c': [3, 4, 5]
    }
    return jsonify(type1)



@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        userpwd=request.form['userpwd']
        print username
        print userpwd
    type2= {
        'title':'登录sssss',
        'a': 1,
        'b': 2,
        'c': [3, 4, 5]
    }
    return jsonify(type2)    


if __name__ == '__main__':
    app.run(debug=True)