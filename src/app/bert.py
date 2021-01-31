import pandas as pd
import glob
from tqdm import tqdm, trange
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
import json
import os

import requests
from flask import Flask, request, Response


from flask_cors import CORS
from requests import Request, Session



import json

import transformers
from transformers import BertForTokenClassification, AdamW

import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import BertTokenizer, BertConfig

from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

from transformers import get_linear_schedule_with_warmup


from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt

import seaborn as sns



app = Flask(__name__)
cors = CORS(app)



@app.route(('/annotate_text'))
def annotate_text():
    
    
  data = request.args.get('text', default='APT', type=str)

  text = []
  for para in data.strip().split('\n\n'):
    para = ' '.join(para.strip().replace("\n", " ").split())
    if para!='':
        text.extend(sent_tokenize(para))
  annotation = []
  
  for test_sentence in text:
    prev_label='O'
    tokenized_sentence = tokenizer.encode(test_sentence)
    input_ids = torch.tensor([tokenized_sentence])#.cuda()
    with torch.no_grad():
        output = model(input_ids)
    label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)
    tokens = tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
    new_tokens, new_labels = [], []
    for token, label_idx in zip(tokens, label_indices[0]):
        if token.startswith("##"):
            new_tokens[-1] = new_tokens[-1] + token[2:]
        else:
            new_labels.append(tag_values[label_idx])
            new_tokens.append(token)
    from nltk import pos_tag
    from nltk.tree import Tree
    from nltk.chunk import conlltags2tree
    tokens = new_tokens
    tags = new_labels
    # tag each token with pos
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
    annotation+=[tokenizer.convert_tokens_to_string(original_text)]
  json_string = json.dumps({'parse':'\n'.join(annotation),'f1_macro':macro_f1[-1], 'prec_macro':macro_prec[-1], 'rec_macro':macro_rec[-1]}, ensure_ascii=False)

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
    LOG_PATH = '../../models/BERT_baseline/'
    
    with open(os.path.join(LOG_PATH,'macro_prec.txt'),'r') as f:
        macro_prec = f.read().strip().split('\n')
    
    with open(os.path.join(LOG_PATH,'macro_rec.txt'),'r') as f:
        macro_rec = f.read().strip().split('\n')
    
    with open(os.path.join(LOG_PATH,'macro_f1.txt'),'r') as f:
        macro_f1 = f.read().strip().split('\n')
    
    tokenizer = BertTokenizer.from_pretrained(os.path.join(LOG_PATH), do_lower_case=False)
    
    model = BertForTokenClassification.from_pretrained(LOG_PATH)
    
    tag_values = ['B-identity',
 'I-malware',
 'B-org',
 'B-industry',
 'I-org',
 'I-city',
 'I-user',
 'B-software',
 'I-cve',
 'B-file',
 'I-mitre_attack',
 'B-theat_actor',
 'I-appdata',
 'B-ioc',
 'B-mitre_attack',
 'B-cve',
 'B-technique',
 'B-name',
 'I-technique',
 'I-program',
 'I-tool',
 'B-user',
 'B-major',
 'B-city',
 'B-appdata',
 'I-identity',
 'I-ioc',
 'O',
 'B-timestamp',
 'B-pid',
 'B-program',
 'I-name',
 'I-country',
 'I-campaign',
 'I-local',
 'B-country',
 'B-campaign',
 'B-local',
 'I-windows',
 'B-attack_pattern',
 'B-excel',
 'B-n',
 'I-timestamp',
 'I-software',
 'I-industry',
 'B-update',
 'B-threat_actor',
 'B-tool',
 'I-type',
 'B-windows',
 'I-file',
 'B-malware',
 'B-type',
 'I-input',
 'B-input',
 'I-threat_actor',
 'PAD']

    app.run(host='0.0.0.0', port=5002)
