#!/bin/sh

HOST=0.0.0.0
PORT=9001
out_dir=parser/model_iss73-5

export CUDA_VISIBLE_DEVICES=-1
echo CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES

nohup python -um web.dp_server --host=$HOST --port=$PORT --out_dir=$out_dir &
