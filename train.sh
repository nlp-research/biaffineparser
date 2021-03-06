#!/bin/bash

#### Set your hyper-parameters here ####
############## START ###################
train_filename=data/sejong.char.train.csv # Path of train dataset.
dev_filename=data/sejong.char.test.csv # Path of dev dataset.
out_dir=parser/model_parser # Store log/model files.
word_embed_file=embeddings/words.pos.original.vec  # Use the pre-trained embedding. If not provided, use random values.
pos_embed_file= #embeddings/words.tag.original.vec  # Use the pre-trained embedding. If not provided, use random values.
char_embed_file= # Use the pre-trained embedding. If not provided, use random values.
num_lstm_layers=4
embed_dropout=0.33
word_embed_size=200  # The embedding dimension for the word's embedding.
pos_embed_size=100  # The embedding dimension for the tag's embedding.
char_embed_size=200 # The embedding dimension for the character's embedding.
arc_mlp_units=600
label_mlp_units=200
num_train_epochs=50 # Num epochs to train.
batch_size=128  # Batch size.
inference_input_file= #data/sejong.char.train.csv
inference_output_file=${out_dir}/sejong.char.test.infer.tsv
device=gpu # device to use
debug=false # use debug mode
word_embed_matrix_file=embeddings/word_embed_matrix.txt
pos_embed_matrix_file=embeddings/pos_embed_matrix.txt
char_embed_matrix_file=embeddings/char_embed_matrix.txt
############## END #####################

[ -d foo ] || mkdir ${out_dir}

export CUDA_VISIBLE_DEVICES=0
echo CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES

echo 'python -m parser.parser'
python -m parser.parser \
    --train_filename=${train_filename} \
    --dev_filename=${dev_filename} \
    --out_dir=${out_dir} \
    --word_embed_file=${word_embed_file} \
    --pos_embed_file=${pos_embed_file} \
    --char_embed_file=${char_embed_file} \
    --num_lstm_layers=${num_lstm_layers} \
    --embed_dropout=${embed_dropout} \
    --word_embed_size=${word_embed_size} \
    --pos_embed_size=${pos_embed_size} \
    --char_embed_size=${char_embed_size}  \
    --arc_mlp_units=${arc_mlp_units} \
    --label_mlp_units=${label_mlp_units} \
    --num_train_epochs=${num_train_epochs} \
    --batch_size=${batch_size} \
    --inference_input_file=${inference_input_file} \
    --inference_output_file=${inference_output_file} \
    --device=${device} \
    --debug=${debug} \
    --word_embed_matrix_file=${word_embed_matrix_file} \
    --pos_embed_matrix_file=${pos_embed_matrix_file} \
    --char_embed_matrix_file=${char_embed_matrix_file}
