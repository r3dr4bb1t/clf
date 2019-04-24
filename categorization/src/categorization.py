# coding=utf-8
import pickle
import re
import time
import csv
import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences





class SimpleTokenizer(object):
    def __init__(self, max_seq_len=25):
          self.stop_words = '롯데백화점,무료배송,정품,현대백화점,하프클럽,추천,개,핫트랙스,바보사랑,아트박스,빠른배송,중고,대,국산,사은품,텐바이텐' \
                          ',할인,방문,가격,인하,개월,할인,매,당일발송,갤러리아'.split(',')

        self.min_word_len = 2

        self.tokenizer = pickle.load(open('./lib/example_tokenizer.pkl', 'rb'))

        self.max_seq_len = max_seq_len

    def filter_name(self, name):
     
        return u' '.join(filter(lambda e: len(e) >= self.min_word_len and e not in self.stop_words,
                                map(lambda i: i.strip(),
                                    re.sub('[!@#$~*+=_:;,.×\(\)\'\[\]\-\/\d]', ' ', name).split(' '))))

    def tokenize(self, name):
       

        filtered = self.filter_name(name=name)

        seq = self.tokenizer.texts_to_sequences([filtered])

        return [pad_sequences(seq, maxlen=self.max_seq_len)]
                

def categorize() :

    test_df = pd.read_csv('./hscrawler/hs.csv')
    test_x = test_df['name'].astype(str)
    column = 'Category'
    test_y = pd.DataFrame(columns = ['Category'])

    cate = []
    prob = []

    idx_cate_dict = pickle.load(open('./lib/example_idx_cate.pkl', 'rb'))
    model = load_model('./lib/example_model.h5')

    tokenizer = SimpleTokenizer()
    for x in test_x:
        test_name = x
        start_time = time.time()
        predict_result = model.predict(tokenizer.tokenize(name=test_name))[0]
        elapsed = time.time() - start_time

        cate.append([idx_cate_dict[np.argmax(predict_result)]])
                topn = 1
        topn_indices = np.argsort(predict_result)[-topn:]
        prob.append((predict_result[topn_indices]))
    test_df['prob'] = prob
    test_df['prob'] = test_df['prob'].str.get(0)
    test_df['Category'] = cate
    test_df['Category'] = test_df['Category'].str.get(0)
    columsOrder = ['date','company','Category','name','url','price','prob']
    test_df=test_df.reindex(columns=columsOrder)

    test_df.to_csv('./categorized.csv',encoding='utf-8',index=False)
 
