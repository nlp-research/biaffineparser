#!/bin/sh

HOST=0.0.0.0
PORT=9001
out_dir=parser/model_iss72-2

nohup python -m web.dp_server --host=$HOST --port=$PORT --out_dir=$out_dir &
