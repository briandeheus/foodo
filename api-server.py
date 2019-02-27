import logging
import lib.redis
import json
import socket

from flask import Flask, request, jsonify, render_template

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
redis_con = lib.redis.get_connection()

hostname = socket.gethostname()


@app.route('/')
def landing():
    print(hostname)
    return render_template('index.html', version=1, hostname=hostname)


@app.route('/api/todos', methods=['get', 'post'])
def todo():

    if request.method == 'POST':
        logging.info('Updating todo => %s', request.json)
        redis_con.rpush('todos', json.dumps(request.json))
        return jsonify({'result': 'ok'})
    else:
        list_id = request.args.get('id')
        todos = redis_con.hgetall(f'{list_id}:todos')

        for t in todos.items():
            print(t)

        return jsonify([json.loads(t.decode()) for k, t in todos.items()])


