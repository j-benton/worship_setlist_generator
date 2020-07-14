# This was adapted from Patrick's flask lesson
import numpy as np
import setlist_gen
from flask import Flask, request, Response, render_template, jsonify

app = Flask('setlist_gen')

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/test')
def test():
    return render_template('setlist.html')

@app.route('/submit')
def submit():
    data = request.args
    verses = [data['Verse 1'], data['Verse 2'], data['Verse 3']]
    themes = data['Themes']
    set_length = int(data['Number of Songs'])
    pw_ratio = int(data['Praise/Worship Songs'])
    setlist = setlist_gen.setlist_generator(verses, themes, set_length, pw_ratio)
    return render_template('setlist.html', songlist=setlist)

if __name__ == '__main__':
    app.run(debug=True)
