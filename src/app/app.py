import requests
from flask import Flask, request, Response
import numpy as np
import pandas as pd
from flask_cors import CORS
from requests import Request, Session
import os


import json

app = Flask(__name__)
cors = CORS(app)




@app.route(('/get_file_list'))
def file_list():
    not_parsed_tags = []
    for i in range(len(not_parsed_texts)):
        not_parsed_tags.append({'DocName':not_parsed_texts.iloc[i]['DocName'],'Stats':{"KeyWords": '', "Sum": 0},'Parsed':False})
    json_string = json.dumps(tags_dicts+not_parsed_tags, ensure_ascii=False)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    return response


@app.route(('/get_file_content'))
def file_content():
    
    filename = request.args.get('filename', default='Group-IB_Lazarus', type=str)
    
    if len(text_stats[text_stats['DocName']==filename])!=0:
        result = {'DocName':filename, 'text':text_stats[text_stats['DocName']==filename]['text'].values[0], 'year':0}
        
    elif len(not_parsed_texts[not_parsed_texts['DocName']==filename])!=0:
        result = {'DocName':filename, 'text':not_parsed_texts[not_parsed_texts['DocName']==filename]['text'].values[0],'year':not_parsed_texts[not_parsed_texts['DocName']==filename]['Year'].values[0]}
    else:
        result = {'DocName':filename, 'text':'', 'year':0}
    
    
    
    json_string = json.dumps(result, ensure_ascii=False)
    response = Response(json_string, content_type="application/json; charset=utf-8")
    return response

@app.route(('/kill_flask'))
def kill_flask():
    raise ValueError('Server was killed')

if __name__ == '__main__':
    DATA_PATH = '../../data/interim'
    
    
    with open(os.path.join(DATA_PATH, 'parsed_text_stats.json'),'r') as f:
        tags_dicts = json.load(f)
    
    text_stats = pd.read_csv(os.path.join(DATA_PATH, 'parsed_text_stats.csv'))
    
    not_parsed_texts = pd.read_csv(os.path.join(DATA_PATH, 'not_parsed_text_stats.csv'))
    

    app.run(host='0.0.0.0', port=5001)
