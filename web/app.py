from flask import Flask, jsonify, request, render_template
from itertools import count
from datetime import datetime
import time
import threading
import json


def load(path):
    result = {}
    last = 0
    try:
        with open(path, 'r') as f:
            for l in f:
                d = json.loads(l)
                result[d['id']] = d
                last = d['id']
    except IOError:
        pass
    
    return result, last + 1;


lock = threading.Lock()
app = Flask(__name__)
data_file = './store.db'

memory, start = load(data_file)
next_index = count(start)


@app.route('/')
def index():
    return 'Hello'


@app.route('/save', methods=['POST'])
def save():
    now = datetime.now()
    now = time.mktime(now.timetuple())
    
    d = dict(request.form)
    d['created_time'] = now
    d['id'] = next_index.next()
    d['user'] = 'yemyat89'
    
    memory[d['id']] = d

    with lock:
        with open(data_file, 'a') as f:
            j = json.dumps(d)
            f.write(j)
            f.write('\n')

    return jsonify(dict(result=True))


@app.route('/view')
def view():
    return jsonify(dict(data=memory))


@app.route('/list_excerpts')
def list_excerpts():
    mem = memory.copy()
    timestamps = {}
    
    for k1 in mem:
        for k2 in mem[k1]:
            d = mem[k1][k2]
            if isinstance(d, list):
                mem[k1][k2] = d[0]
            elif isinstance(d, float):
                g = datetime.fromtimestamp(d)
                mem[k1][k2] = g.strftime('%d/%m/%Y %H:%M')
                timestamps[k1] = d
    
    return render_template('list.html', data=mem, ts=timestamps)

@app.route('/detail_excerpt/<rid>')
def detail(rid):
    d = memory[int(rid)]
    return render_template('detail_excerpt.html', d=d) 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
