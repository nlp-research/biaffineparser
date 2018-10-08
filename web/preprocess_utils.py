import re


def get_dataset_from_sentence(analyzed_input, eoj_delim=' + ', morph_delim=' '):

    maxlen = 0
    maxwordlen = 0
    maxcharlen = 0

    sent_tokens = ['ROOT_START']
    char_tokens = ['ROOT_START']
    pos_tokens = ['ROOT_START']

    # 어절 분할
    eojs = analyzed_input.split(eoj_delim)
    sent_tokens += [eoj.replace(morph_delim, '|') for eoj in eojs]  # 형태소/태그
    pos_tokens += ['|'.join([morph.rsplit('/', 1)[1]
                             for morph in eoj.split(morph_delim)]) for eoj in eojs]  # 태그
    char_tokens += ['|'.join(['|'.join(morph.rsplit('/', 1)[0])
                              for morph in eoj.split(morph_delim)]) for eoj in eojs]  # 음절

    # maxlen = len(eojs)  # 최대 어절 길이
    maxlen = len(sent_tokens)  # 최대 어절 길이
    maxwordlen = max([len(eoj.split('|')) for eoj in sent_tokens])  # 최대 형태소 개수
    maxcharlen = max([len(chars.split('|'))
                      for chars in char_tokens])  # 최대 음절 개수

    return [sent_tokens], [pos_tokens], [char_tokens], maxlen, maxwordlen, maxcharlen


if __name__ == '__main__':
    result = get_dataset_from_sentence(
        '형태소/NNG 를/JKO + 입력/NNG 하/XSV ㄹ게/EFN + 좀/MAG + 변환/NNG 하/XSV 어/ECS 주/VXV 어/ECS')
    print(result)
    exit()
