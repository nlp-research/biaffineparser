#!/bin/sh

HOST=0.0.0.0
PORT=9000

nohup python -u morph_server.py --host=$HOST --port=$PORT &