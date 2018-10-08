# -*- coding: utf-8 -*-
import argparse
import json
from parser.biaffineparser import BiaffineParser

from flask import Flask, jsonify, request

from web.preprocess_utils import get_dataset_from_sentence

app = Flask(__name__)
app.json_encoder.ensure_ascii = True
app.config['JSON_AS_ASCII'] = False

FLAGS = None
parser = None


def add_arguments(parser):
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help="host to run morph analyzer server")
    parser.add_argument('--port', type=int, default=9000,
                        help="port to run morph analyzer server")
    parser.add_argument("--out_dir", type=str, default=None,
                        help="Store log/model files.")


@app.route('/')
def hello_world():
    return '/dp'


@app.route('/sample')
def sample():
    sentence = '형태소/NNG 를/JKO + 입력/NNG 하/XSV ㄹ게/EFN + 좀/MAG + 변환/NNG 하/XSV 어/ECS 주/VXV 어/ECS'
    arc, label = parser.parse(
        sentence, get_dataset_from_sentence)
    result = {'sentence': sentence, 'arc': arc.tolist(), 'label': label}
    return jsonify(result)


@app.route('/dp', methods=['POST'])
def parse():
    if request.method == 'GET':
        try:
            request_json = request.args.get('json')
            parsed_json = json.loads(request_json)
            sentence = parsed_json.get('sentence', '')
        except Exception as e:
            return f'Error: {e}'
    else:
        sentence = request.json.get('sentence', '')
    arc, label = parser.parse(
        sentence,
        get_dataset_from_sentence)
    result = {'sentence': sentence, 'arc': arc.tolist(), 'label': label}
    return jsonify(result)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    add_arguments(argparser)
    FLAGS = argparser.parse_args()
    parser = BiaffineParser(FLAGS.out_dir)
    app.run(host=FLAGS.host, port=FLAGS.port, debug=False)
