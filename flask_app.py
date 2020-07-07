import numpy as np
import pickle
from flask import Flask, request, Response, render_template, jsonify

app = Flask('setlist_gen')

@app.route('/')
def home():
    return 'Come on, somebody!'

@app.route('/hc_page')
def hc_page():
    return "<html><body><h1>I don\'t know what I\'m doing!</h1><p>But I\'m learning!</p></body></html>"

@app.route('/some_json')
def some_json():
    best_things = {
    'food': 'pasta salad',
    'soda': 'ginger ale',
    'board game': 'chess'
    }
    return jsonify(best_things)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit')
def submit():
    data = request.args
    return jsonify(request.args)


if __name__ == '__main__':
    app.run(debug=True)
