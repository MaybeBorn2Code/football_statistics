from flask import Flask, render_template, request, flash, redirect, url_for, abort
from services import Connection
import requests


app = Flask(__name__)
conn: Connection = Connection()
conn.create_tables()
app.config['SECRET_KEY'] = 'your secret key'
URL = 'https://raw.githubusercontent.com/openfootball/football.json/master/2020/jp.1.json'

# adding game score
def add_score() -> list:
    request_ = requests.get(URL)
    text_ = request_.json()
    for i in (text_['matches']):
        try:
            conn.add_score(str(i['score']['ft']).replace('[','').replace(']','').replace(', ',':'))
        except:
            conn.add_score((str('None')))

# adding teams, date, rounds
def squad_add():
    request_ = requests.get(URL)
    text_ = request_.json()
    for i in text_['matches']:
        conn.insert_into_overall(round=(i['round']),date=(i['date']),first_team=(i['team1']),second_team=(i['team2']))

# adding to third table id
def connect_to():
    request_ = requests.get(URL)
    text_ = request_.json()
    count = 0
    for i in text_['matches']:  
        count += 1
        conn.insert_overall(int(count),int(count))

@app.route('/', methods=['POST', 'GET'])
def login():
    add_score()
    squad_add()
    connect_to()
    show_info = conn.show_all_information()
    if request.method == 'POST':
        global find_score
        find_score = request.form["score"]
        if find_score:
            return redirect(url_for('score_info'))
        else:
            flash('Nothing entered', 'info')
    return render_template('login.html', title='Final', show = show_info)

@app.route('/score_info', methods=['POST', 'GET'])
def score_info():
    score_information = conn.show_score_information(score=find_score)
    return render_template('score.html', title = 'Score info', score_information = score_information)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
    