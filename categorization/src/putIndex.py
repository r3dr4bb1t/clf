
from elasticsearch import  helpers, Elasticsearch
import csv
def putIndex():
    es = Elasticsearch()
  
  
 
    #with open(output, encoding='utf-8') as f: 
    #requests.put('http://localhost:9200/hscate/')

    #with open('mapping.json','rb') as data:
     #   headers = {'content-type': 'application/json'}
      #  requests.put('http://localhost:9200/hscate/class/_mapping', data=data, headers=headers)

    with open('./categorized.csv','rt',encoding='utf-8') as f:
     #   headers = {'content-type': 'application/json'}
      #  requests.put('http://localhost:9200/hscate/class/_bulk', data=data, headers=headers)

        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='hscate', doc_type='class')
