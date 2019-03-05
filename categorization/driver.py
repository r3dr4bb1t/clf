import pandas as pd
import json
import sys
import os
import requests
from src import categorization, putIndex, queryHandler
from flask import Flask, render_template, request, url_for, redirect
from pprint import pprint


app = Flask(__name__)

#pprint(data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crawl',methods=['POST'])
def crawl():
    os.system('cd hscrawler && scrapy crawl hsSpider')
    return 'Crawled successfully, Check ./hscrawler/hs.csv !'

@app.route('/categorize',methods=['POST'])
def cate():
    categorization.categorize()
    return 'Categorized successfully, Check ./Categorized.csv !'

@app.route('/indexing', methods=['POST'])
def index():
    putIndex.putIndex()
    return 'Indexed successfully, Check "http://localhost:9200/hscate"'

@app.route('/delete_index',methods=['GET','DELETE'])
def cateDelete():
    if request.method == 'GET':
        return render_template('index.html')
    else :
        requests.delete('http://localhost:9200/hscate/')
        return 'deleted'


@app.route('/query', methods=['POST'])
def query():
    params = request.form['text']
    return (queryHandler.queryHandler(params).to_json(orient='records',force_ascii=False))


if __name__ == '__main__':
    app.debug = True
    app.run()