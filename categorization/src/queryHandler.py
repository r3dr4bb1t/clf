from elasticsearch import Elasticsearch
import pandas as pd
import csv
#from categorization import putIndex

def queryHandler(params):
    es = Elasticsearch()
    name = params.split(',')[0]

    cateprob = {}
    for cate in params.split(',')[1:]:
        cateprob[cate.split(':')[0]]=cate.split(':')[1]
    res = es.search(body={'size':'10000','query': { 
        'function_score': {
            'query': {
                'match': {
                    'name': name
                }
            } ,
        'script_score': {  
            'script' : { 
                'params' : {
                    'cateprob' : cateprob
                },
            'inline' : '_score'
            #'inline' : '_score + cateprob[doc["Category"]]*doc["prod"]'
            }
           # 'inline' : '_score + cateprob[여행]'
        } 
    }
    }})
    print(res['hits']['hits'])
    basescore=[]
#print (res['hits']['hits'])
    for i in (res['hits']['hits']):
        basescore.append((i['_score']))
#print(basescore)

   # with open('df.json','w',encoding='utf-8') as f:
   # with open('df.json','w',encoding='utf-8') as f:

    with open('./queryRes.csv', 'w',encoding='utf-8',newline='') as f:  # Just use 'w' mode in 3.x
        header_present  = False
        for doc in res['hits']['hits']:
            my_dict = doc['_source'] 
            if not header_present:
                w = csv.DictWriter(f, my_dict.keys())
                w.writeheader()
                header_present = True
            w.writerow(my_dict)
    score = []
    queryRes = pd.read_csv('./queryRes.csv')
    prob = queryRes['prob'].astype(float)
    cateprob = queryRes['Category'].map(cateprob).astype(float)
    weight = 100
    pd.DataFrame(columns = ['Score'])
    score = basescore + (prob* cateprob * weight)
    queryRes['Score']=score

    queryRes = queryRes.dropna()
    queryRes.sort_values('Score')

    queryRes = queryRes.drop_duplicates(subset=['name'], keep='first')
    return queryRes.sort_values('Score', ascending=False)

#print(queryRes['Score'])
#pd.DataFrame(columns = ['Score'])
#score = basescore+ (prob * int(cateprob[category]))
##queryRes['Score'] = score 
#p#rint(score)
   # test_df['prob'] = prob
    #test_df['prob'] = test_df['prob'].str.get(0)
    #test_df['Category'] = cate
    #test_df['Category'] = test_df['Category'].str.get(0)
    #columsOrder = ['date','company','Category','name','url','price','prob']
    #test_df=test_df.reindex(columns=columsOrder)

    #test_df.to_csv('./categorized.csv',encoding='utf-8',index=False)
   # with open('df.json','w',encoding='utf-8') as f:
