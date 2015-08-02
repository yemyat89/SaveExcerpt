from flask import Flask, jsonify, request, render_template
from itertools import count
from datetime import datetime
import time
from copy import deepcopy
import json
from pymongo import MongoClient


username = None
password = None

lines = []
with open('../auth.data', 'r') as f:
    for l in f:
        lines.append(l[:-1])

assert len(lines) == 2

username = lines[0]
password = lines[1]

connection = MongoClient("ds041150.mongolab.com", 41150)
db = connection["excerptdb_ymt"]
db.authenticate(username, password)

user_db = db.users
excerpt_db = db.excerpts

app = Flask(__name__)

start = excerpt_db.count() + 10
next_index = count(start)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def index():
    return 'Hello'


@app.route('/save', methods=['POST'])
def save():
    now = datetime.now()
    now = time.mktime(now.timetuple())
    
    d = dict(request.form)
    
    excerpt_data = {'about': d['about'][0],
                    'url': d['url'][0],
                    'title': d['title'][0],
                    'excerpt': d['excerpt'][0]}
    excerpt_data['created_time'] = now
    excerpt_data['id'] = next_index.next()
    
    excerpt_data['username'] = 'yemyat89'
    
    excerpt_db.insert(excerpt_data)

    return jsonify(dict(result=True))


@app.route('/view')
def view():
    d = [x for x in excerpt_db.find()]
    for x in d:
        x.pop('_id')
    return jsonify(dict(data=d))


@app.route('/list_excerpts')
def list_excerpts():
    timestamps = {}
    mem2 = [x for x in excerpt_db.find()]
    
    for i, x in enumerate(mem2):
        for k, v in x.iteritems():
            if isinstance(v, float):
                g = datetime.fromtimestamp(v)
                mem2[i][k] = g.strftime('%d/%m/%Y %H:%M')
                timestamps[i] = v
    
    return render_template('list.html', data=mem2, ts=timestamps)

@app.route('/detail_excerpt/<rid>')
def detail(rid):
    d = excerpt_db.find_one({'id': int(rid)})
    rel_url = [x for x in excerpt_db.find({"$and": [{"url": d['url']}, {"id": {"$ne": d['id']}}]})]
    for i, x in enumerate(rel_url):
        g = datetime.fromtimestamp(x['created_time'])
        rel_url[i]['created_time'] = g.strftime('%d/%m/%Y %H:%M')
    return render_template('detail_excerpt.html', d=d, rel=rel_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
