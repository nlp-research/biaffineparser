# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from konlpy.tag import Kkma
from flask import request
import argparse
import json

app = Flask(__name__)
app.json_encoder.ensure_ascii = True
app.config['JSON_AS_ASCII'] = False

FLAGS = None

#add arguments
def add_arguments(parser):
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help="host to run morph analyzer server")
    parser.add_argument('--port', type=int, default=9000,
                        help="port to run morph analyzer server")
#hello world
@app.route('/')
def hello_world():
    return 'Hello, World!'

#analyze morph
@app.route('/morph/analyze', methods=['POST', 'GET'])
def analyze():
    tagger = Kkma()
    if request.method == 'GET':
        try:
            request_json = request.args.get('json')
            parsed_json = json.loads(request_json)
            sentence = parsed_json.get('sentence', '')
        except Exception as e:
            return f'Error: {e}'
    else:
        sentence = request.json.get('sentence', '')
    pos_result = tagger.pos(sentence, flatten=False, join=True)
    pos_result = ['+'.join(s) for s in pos_result]
    return jsonify(pos_result)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    add_arguments(argparser)
    FLAGS = argparser.parse_args()
    app.run(host=FLAGS.host, port=FLAGS.port, debug=True)
    