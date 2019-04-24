
from elasticsearch import  helpers, Elasticsearch
import csv
def putIndex():
    es = Elasticsearch()

    with open('./categorized.csv','rt',encoding='utf-8') as f:
    
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='hscate', doc_type='class')
