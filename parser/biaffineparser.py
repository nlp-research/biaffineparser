# -*- coding: utf-8 -*-
import json
import os
from parser import utils
from parser.model import Model


class Hparams(object):
    def __init__(self, adict):
        self.__dict__.update(adict)


class BiaffineParser(object):
    def __init__(self, model_dir):
        flags = self._load_hparams(model_dir)

        self.words_dict = utils.load_vocab(os.path.join(
            flags.out_dir, flags.word_vocab_name))
        self.pos_features_dict = utils.load_vocab(os.path.join(
            flags.out_dir, flags.pos_vocab_name))
        self.char_features_dict = utils.load_vocab(os.path.join(
            flags.out_dir, flags.char_vocab_name))
        rels_features_dict = utils.load_vocab(os.path.join(
            flags.out_dir, flags.rel_vocab_name))
        heads_features_dict = utils.load_vocab(os.path.join(
            flags.out_dir, flags.head_vocab_name))

        word_embedding, _ = utils.load_embed_model(
            flags.word_embed_file, self.words_dict, flags.word_embed_size)
        pos_embedding, _ = utils.load_embed_model(
            flags.pos_embed_file, self.pos_features_dict, flags.pos_embed_size)
        char_embedding, _ = utils.load_embed_model(
            flags.char_embed_file, self.char_features_dict, flags.char_embed_size)

        self.model = Model(
            flags,
            self.words_dict,
            self.char_features_dict,
            self.pos_features_dict,
            rels_features_dict,
            heads_features_dict,
            word_embedding,
            char_embedding,
            pos_embedding,
            'infer')

        self.model.new_sess_and_restore(
            os.path.join(flags.out_dir, 'parser.ckpt'))

    def parse(self, sentence):
        sentences = [['ROOT_START', '내/NP|가/JKS', '사건/NNG|들/XSN|을/JKO',
                      '어거/NNG|(/SS|馭/SH|車/SH|)/SS|하/XSV|아/EC', '오/VX|았/EP|다고/EC|는/JX', '주장/NNG|하/XSV|ㄹ/ETM', '수/NNB', '없/VA|습니다/EF|./SF']]
        pos = [['ROOT_START', 'NP|JKS', 'NNG|XSN|JKO', 'NNG|SS|SH|SH|SS|XSV|EC',
                'VX|EP|EC|JX', 'NNG|XSV|ETM', 'NNB', 'VA|EF|SF']]
        chars = [['ROOT_START', '내|가', '사|건|들|을',
                  '어|거|(|馭|車|)|하|아', '오|았|다|고|는', '주|장|하|ㄹ', '수', '없|습|니|다|.']]
        maxlen = 8
        maxwordlen = 7
        maxcharlen = 8

        sentences_indexed = utils.get_indexed_sequences(
            sentences, self.words_dict, maxlen, maxwordl=maxwordlen, split_word=True)
        char_indexed = utils.get_indexed_sequences(
            chars, self.char_features_dict, maxlen, maxwordl=maxcharlen, split_word=True)
        pos_indexed = utils.get_indexed_sequences(
            pos, self.pos_features_dict, maxlen, maxwordl=maxwordlen, split_word=True)

        data = (sentences_indexed, char_indexed, pos_indexed)

        result = self.model.inference_step(data)
        (head_preds, rel_preds_ids) = result

        rev_vocab_rels = {i: w for w, i in (
            self.model.rels_vocab_table.items())}
        rel_preds = [rev_vocab_rels[i] for i in rel_preds_ids]

        return head_preds, rel_preds

    def _load_hparams(self, model_dir):
        fp = os.path.join(model_dir, 'hparams.json')
        print('=' * 30)
        print(f'Loading parameters... {fp}')
        flags = json.load(open(fp))
        print(flags)
        return Hparams(flags)


if __name__ == '__main__':
    parser = BiaffineParser('parser/model_iss72-2')
    result = parser.parse('안녕')
    print(result)
