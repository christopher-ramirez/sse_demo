#!/usr/bin/env python

import gevent
import gevent.monkey
import werkzeug.serving
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template

app = Flask(__name__)

def event_stream():
    count = 0
    while True:
        gevent.sleep(2)
        yield 'data: %s\n\n' % count
        count += 1

@app.route('/event_source')
def sse_request():
    return Response(
            event_stream(),
            mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('sse.html')


@werkzeug.serving.run_with_reloader
def run_server():
    app.debug = True

    http_server = WSGIServer(('127.0.0.1', 8001), app)
    http_server.serve_forever()

if __name__ == '__main__':
    run_server()