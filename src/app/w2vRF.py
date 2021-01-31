import pandas as pd
import glob
from nltk import word_tokenize, pos_tag, ne_chunk
from tqdm import tqdm, trange
from nltk.tokenize import sent_tokenize
import numpy as np

from gensim.models import Word2Vec

import requests
from flask import Flask, request, Response


from flask_cors import CORS
from requests import Request, Session



import json

import matplotlib.pyplot as plt

import seaborn as sns



app = Flask(__name__)
cors = CORS(app)



@app.route(('/annotate_text'))
def annotate_text():
    
    
  data = request.args.get('text', default='APT', type=str)

  from nltk.chunk import conlltags2tree
  from nltk import pos_tag
  from nltk.tree import Tree
  annotation = []
  
  for test_sentence in data['Sentence']:
    prev_label='O'
    
    def preprocess_words(x):

        x = x.lower()
        x = '_'.join(x.split(' ')[:2])
        x = '_'.join(x.split('-')[:2])
        return x
    def feature_map(word):
      

      word = preprocess_words(word)

      try:
        return model.wv[word]
      except KeyError:
        return np.zeros(100,)
    
    tokenized_sentence = [feature_map(x) for x in test_sentence.split(' ')]
    
    tags = rf.predict(tokenized_sentence)
    tokens = [preprocess_words(x) for x in test_sentence.split(' ')]
    pos_tags = [pos for token, pos in pos_tag(tokens)]
    # convert the BIO / IOB tags to tree
    conlltags = [(token, pos, tg) for token, pos, tg in zip(tokens, pos_tags, tags)]
    ne_tree = conlltags2tree(conlltags)
    # parse the tree to get our original text
    original_text = []
    for subtree in ne_tree:
        # checking for 'O' tags
        if type(subtree) == Tree:
            original_label = subtree.label()
            original_string = " ".join([token for token, pos  in subtree.leaves()])
            if (original_string!='[CLS]' and original_string!='[SEP]'):
              if original_label==prev_label:
                original_text.append(original_string)
              else:
                original_text.append('<'+original_label.upper()+'>'+original_string)
              prev_label = original_label
        elif type(subtree)==tuple:
          if (subtree[0]!='[CLS]' and subtree[0]!='[SEP]'):
            if prev_label!='O':
              original_text[-1]+='</'+original_label.upper()+'>'
              prev_label='O'
            original_text.append(subtree[0])
    annotation+=[' '.join(original_text)]
  json_string = json.dumps({'parse':'\n'.join(annotation),'f1_macro':0.24, 'prec_macro':0.31, 'rec_macro':0.21}, ensure_ascii=False)

  response = Response(json_string, content_type="application/json; charset=utf-8")
  return '\n'.join(annotation)


@app.route(('/kill_flask'))
def kill_flask():
    raise ValueError('Server was killed')

if __name__ == '__main__':
    
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    
    DATA_PATH = '../../data/processed/'
    LOG_PATH = '../../models/W2Vec_100_RF_20'
    
    from gensim.models import Word2Vec
    model = Word2Vec.load(os.path.join(LOG_PATH,"word2vec.model_100"))

    rf = joblib.load( os.path.join(LOG_PATH,"random_forest.joblib"))

    app.run(host='0.0.0.0', port=5005)
