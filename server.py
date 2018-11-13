from gevent import monkey
monkey.patch_all()

import threading
import time
from flask import Flask, abort, jsonify, request, send_from_directory
from gevent.pywsgi import WSGIServer
from uuid import uuid4

app = Flask(__name__)

cvPut = threading.Condition()
cvGet = threading.Condition()

workers = 0

tasks = {}
pending = []
doing = []
done = []

def main(address="0.0.0.0", port=3333):
    http_server = WSGIServer((address, port), app)
    http_server.serve_forever()

@app.route("/")
def root():
    return f"<html><head><title>Geetest 3.0 - Status</title><meta http-equiv=\"refresh\" content=\"5\"></head><body>Geetest 3.0 Distributed Cracking Platform<br/>Developed by <a href=\"https://github.com/Hsury\">HsuRY</a><br/><br/>Workers: {workers + len(doing)}<br/><br/>Pending: {len(pending)}<br/>Doing: {len(doing)}<br/>Done: {len(done)}</body></html>"

@app.route("/crack")
def crack():
    if all([key in request.args for key in ['gt', 'challenge']]):
        session = str(uuid4())
        tasks[session] = {
            'code': -1,
            'gt': request.args.get('gt'),
            'challenge': request.args.get('challenge'),
            'success': request.args.get('success', 1),
            'validate': "",
            'seccode': "",
        }
        pending.append(session)
        with cvPut:
            cvPut.notify_all()
        with cvGet:
            if cvGet.wait_for(lambda: session in done, timeout=30):
                # done.remove(session)
                if tasks[session]['code'] == 0:
                    return jsonify({
                        'code': 0,
                        'message': "success",
                        'challenge': tasks[session]['challenge'],
                        'validate': tasks[session]['validate'],
                        'seccode': tasks[session]['seccode'],
                    })
                else:
                    return jsonify({
                        'code': -2,
                        'message': "error",
                    })
            else:
                if session in pending:
                    pending.remove(session)
                if session in doing:
                    doing.remove(session)
                done.append(session)
                return jsonify({
                    'code': -3,
                    'message': "timeout",
                })
        del tasks[session]
    else:
        return jsonify({
            'code': -1,
            'message': "invalid parameter",
        })

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route("/feedback", methods=['POST'])
def feedback():
    if all([key in request.form for key in ['session', 'code']]):
        session = request.form.get('session')
        if session in doing:
            if request.form.get('code') == "0" and all([key in request.form for key in ['challenge', 'validate', 'seccode']]):
                tasks[session]['code'] = 0
                tasks[session]['challenge'] = request.form.get('challenge')
                tasks[session]['validate'] = request.form.get('validate')
                tasks[session]['seccode'] = request.form.get('seccode')
            doing.remove(session)
            done.append(session)
            with cvGet:
                cvGet.notify_all()
            return jsonify({
                'code': 0,
                'message': "success",
            })
        else:
            return jsonify({
                'code': -2,
                'message': "invalid session",
            })
    else:
        return jsonify({
            'code': -1,
            'message': "invalid parameter",
        })

@app.route("/fetch")
def fetch():
    global workers
    workers += 1
    with cvPut:
        if cvPut.wait_for(lambda: pending, timeout=15):
            session = pending.pop(0)
            doing.append(session)
            workers -= 1
            return jsonify({
                'session': session,
                'gt': tasks[session]['gt'],
                'challenge': tasks[session]['challenge'],
                'success': tasks[session]['success'],
            })
        else:
            workers -= 1
            abort(503)

@app.route("/status")
def status():
    return jsonify({
        'code': 0,
        'workers': workers + len(doing),
        'pending': len(pending),
        'doing': len(doing),
        'done': len(done),
    })

@app.route("/task")
def task():
    return app.send_static_file("geetest.html")

if __name__ == "__main__":
    main()
