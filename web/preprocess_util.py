import re

def get_dataset_from_sentence(analyzed_input):

    maxlen = 0
    maxwordlen = 0
    maxcharlen = 0

    single_sent = ['ROOT_START']
    single_chars = ['ROOT_START']
    single_pos = ['ROOT_START']
    
    eojs = analyzed_input.split(' + ')
    
    single_sent = [eoj.replace(' ', '|') for eoj in eojs]
    single_pos = ['|'.join([morph.rsplit('/', 1)[1] for morph in eoj.split(' ')]) for eoj in eojs]
    single_chars = ['|'.join(['|'.join(morph.rsplit('/', 1)[0]) for morph in eoj.split(' ')]) for eoj in eojs]
    maxlen = len(single_sent)
    maxwordlen = max([len(eoj.split('|')) for eoj in single_sent])
    maxcharlen = max([len(chars.split('|')) for chars in single_chars])
    
    return [single_sent], [single_pos], [single_chars], maxlen, maxwordlen, maxcharlen

if __name__ == '__main__':
    
    exit()
    