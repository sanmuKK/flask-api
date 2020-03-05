from flask_redis import FlaskRedis
from flask import Flask,jsonify,request,url_for,abort,redirect,Response
import datetime,json


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://127.0.0.1:6379/0"
app.config['JSON_SORT_KEYS'] = False
rd = FlaskRedis(app)
rd.flushall()


@app.route('/')
def index():
    return redirect(url_for('get_tasks'))


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def wrong(error):
    return jsonify({'error': 'Bad Request'}), 500


@app.route('/todo/api/v1.0/tasks',methods=['GET'])
def get_tasks():
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        res = {
            "status": 0,
            "message": "",
            "data": [json.loads(v) for v in msgs]
        }
    else:
        res = {
            "status": 1,
            "message": "no data",
            "data": []
        }
    resp = json.dumps(res, ensure_ascii=False)
    return Response(resp, mimetype="application/json")


@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['GET'])
def get_task(task_id):
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        r = []
        for i in msgs:
            if json.loads(i)['id'] == task_id:
                r.append(i)
                break
        if r:
            res = {
                "status": 0,
                "message": "",
                "data": [json.loads(v) for v in r]
                }
        else:
            res = {
                "status": 1,
                "message": "no found",
                "data": []
            }
    else:
        res = {
            "status": 1,
            "error": "no data",
            "data": []
        }
    resp = json.dumps(res, ensure_ascii=False)
    return Response(resp, mimetype="application/json")


@app.route('/todo/api/v1.0/tasks/finished',methods=['GET'])
def get_finished_tasks():
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        r = []
        for i in msgs:
            if json.loads(i)['done'] == 'finished':
                r.append(i)
        res = {
            "status": 0,
            "message": "",
            "data": [json.loads(v) for v in r]
        }
    else:
        res = {
            "status": 1,
            "message": "error or no data",
            "dapip freeze>requirements.txtta": []
        }
    resp = json.dumps(res, ensure_ascii=False)
    return Response(resp, mimetype="application/json")


@app.route('/todo/api/v1.0/tasks/not_finished',methods=['GET'])
def get_not_finished_tasks():
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        r = []
        for i in msgs:
            if json.loads(i)['done'] == 'not finished':
                r.append(i)
        res = {
            "status": 0,
            "message": "",
            "data": [json.loads(v) for v in r]
        }
    else:
        res = {
            "status": 1,
            "message": "error or no data",
            "data": []
        }
    resp = json.dumps(res, ensure_ascii=False)
    return Response(resp, mimetype="application/json")


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'todo' in request.json:
        abort(404)
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, 0)
        for i in msgs:
            id = json.loads(i)['id'] + 1
    else:
        id = 1
    try:
        ddl = request.json['ddl']
    except:
        ddl = (datetime.datetime.now()+datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    task = {
        'id': id,
        'done': 'not finished',
        'todo': request.json.get('todo', ""),
        'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ddl': ddl
    }
    resp = json.dumps(task)
    rd.lpush("memo", resp)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/finished/<int:task_id>', methods=['PUT'])
def finished_task(task_id):
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        length = 0
        for i in msgs:
            if json.loads(i)['id'] > task_id:
                length = length + 1
        for i in msgs:
            if json.loads(i)['id'] == task_id:
                id = json.loads(i)['id']
                ddl = json.loads(i)['ddl']
                todo = json.loads(i)['todo']
                add_time = json.loads(i)['add_time']
                task = {
                'id': id,
                'done': 'finished',
                'todo': todo,
                'add_time': add_time,
                'ddl': ddl
                }
                resp = json.dumps(task)
                rd.lset("memo",length,resp)
                return jsonify({'result': True})
    abort(404)


@app.route('/todo/api/v1.0/tasks/not_finished/<int:task_id>', methods=['PUT'])
def not_finished_task(task_id):
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        length = 0
        for i in msgs:
            if json.loads(i)['id'] > task_id:
                length = length + 1
        for i in msgs:
            if json.loads(i)['id'] == task_id:
                id = json.loads(i)['id']
                ddl = json.loads(i)['ddl']
                todo = json.loads(i)['todo']
                add_time = json.loads(i)['add_time']
                task = {
                    'id': id,
                    'done': 'not finished',
                    'todo': todo,
                    'add_time': add_time,
                    'ddl': ddl
                }
                resp = json.dumps(task)
                rd.lset("memo", length, resp)
                return jsonify({'result': True})
    abort(404)


@app.route('/todo/api/v1.0/tasks/finished_all',methods=['PUT'])
def finished_all():
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        flag = 0
        for i in msgs:
            length = 0
            for k in msgs:
                if json.loads(k)['id'] > json.loads(i)['id']:
                    length = length + 1
            if json.loads(i)['done'] == 'not finished':
                id = json.loads(i)['id']
                ddl = json.loads(i)['ddl']
                todo = json.loads(i)['todo']
                add_time = json.loads(i)['add_time']
                task = {
                'id': id,
                'done': 'finished',
                'todo': todo,
                'add_time': add_time,
                'ddl': ddl
                }
                resp = json.dumps(task)
                rd.lset("memo", length, resp)
                flag = 1
            else:
                continue
        if flag == 0:
            abort(404)
    else:
        abort(500)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tasks/not_finished_all',methods=['PUT'])
def not_finished_all():
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        flag = 0
        for i in msgs:
            length = 0
            for k in msgs:
                if json.loads(k)['id'] > json.loads(i)['id']:
                    length = length + 1
            if json.loads(i)['done'] == 'finished':
                id = json.loads(i)['id']
                ddl = json.loads(i)['ddl']
                todo = json.loads(i)['todo']
                add_time = json.loads(i)['add_time']
                task = {
                    'id': id,
                    'done': 'not finished',
                    'todo': todo,
                    'add_time': add_time,
                    'ddl': ddl
                    }
                resp = json.dumps(task)
                rd.lset("memo", length, resp)
                flag = 1
            else:
                continue
        if flag == 0:
            abort(404)
    else:
        abort(500)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        for i in msgs:
            if json.loads(i)['id'] == task_id:
                rd.lrem(key, 1, i)
                break
    else:
        abort(404)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tasks/delete/finished',methods=['DELETE'])
def del_all_finished_tasks():
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        for i in msgs:
            if json.loads(i)['done'] == "finished":
                rd.lrem(key, 1, i)
    else:
        abort(404)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tasks/delete/not_finished',methods=['DELETE'])
def del_all_not_finished_tasks():
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        for i in msgs:
            if json.loads(i)['done'] == "not finished":
                rd.lrem(key, 1, i)
    else:
        abort(404)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tasks/delete/all',methods=['DELETE'])
def del_all_tasks():
    key = 'memo'
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        for i in msgs:
            rd.lrem(key, 1, i)
    else:
        abort(404)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tasks/quantity')
def quantities():
    key = 'memo'
    finished = 0
    not_finished = 0
    if rd.llen(key):
        msgs = rd.lrange(key, 0, -1)
        for i in msgs:
            if json.loads(i)['done'] == 'finished':
                finished = finished + 1
        not_finished = rd.llen(key) - finished
    all_task = rd.llen(key)
    quantity = {
        'all_quantity': all_task,
        'finished': finished,
        'not_finished': not_finished
        }
    resp = json.dumps(quantity, ensure_ascii=False)
    return Response(resp, mimetype="application/json")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8787)