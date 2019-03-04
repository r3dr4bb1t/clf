### 검색 시스템 개발 프로젝트 - 노민수
 
##### 1. 개발 환경 
Windows 10, Python 3.7
##### 2. 구동 환경
localhost:5000(flask), localhost:9200(elasticsearch)
##### 3. 테스트 방법  
---  
1. 라이브러리 설치
```console  
~$ pip3 install requests, flask, scrapy, elasticsearch-py, numpy, pandas
```
2. [elasticsearch 설치](https://www.elastic.co/kr/downloads/elasticsearch)  

3. elasticsearch 실행, localhost:9200
```console
~$ ./elasticsearch
```
4. ./driver.py 실행, localhost:5000 접속.
```console
~$ ./python driver.py
```
5. 버튼 순서 : **Crawl**(3~5분 소요) -> **Categorization** -> **Indexing** -> **이름, 카테고리 통계** 쿼리 입력 (ex 일본 / 여행 0.8, 식품 0.2) 
6. 쿼리 후 결과는 리턴되는 웹 페이지에서 확인  

##### 3. 코드 진행
1. hsmoa.com 에서 30일 치 데이터(date, company, name, url, price)를  scrapy로 크롤링(crawler.py) 후, hs.csv 파일로 저장.
2. categorization.py 의 categorize() 함수에서 hs.csv 를 읽은 후 **카테고리 분류 진행** 후, 그 값들을 *category*라는 새로운 칼럼으로 넣어 categorization.csv로 저장.
3. 뒤에서 사용될  base score를 위해, 위 함수에서 해당 상품의 (카테고리 일치 확률값*100)을 *base score*라는 새로운 칼럼으로 넣어 categorization.csv로 저장.
4.  indexing.py 의 putIndex()에서 categorization.csv를 읽어서 localhost:9200/hscate 인덱스 생성 및 데이터 벌크로 추가

5.  주어진 100개의 데이터로 쿼리가 입력될 것으로 예상 (ex 일본, 여행 : 0.8, 식품 : 0.2), *match = *query's product name* && category = *query's category name**으로 es에 쿼리 후, hits 중 제일 높은 *base score*를 가진 것들에  쿼리의 카테고리 확률(ex 여행 : 0.8,  식품 : 0.2)과 alpha의 곱을 더함.(top base score hits + (alpha * query's category))  
##### 4. 테스트 방법
1. dependencies : requests, flask, scrapy, elasticsearch-py, numpy, pandas, elasticsearch 설치
2. elasticsearch 실행, localhost:9200
3. Categorization/driver.py 실행, localhost:5000 접속.
4. 버튼 순서 : Crawl(3~5분 소요) -> Categorization -> Indexing -> **이름, 카테고리 통계** 쿼리 입력 (ex 일본 / 여행 0.8, 식품 0.2) 
5. 쿼리 후 결과는 리턴되는 웹 페이지에서 확인  



##### 5. 기타
* ES : AWS elasticsearch service나 Elasticsearch cloud로 진행하면 난이도 하향 및 개발적인 요소가 많이 사라질 것 같아 로컬에서 진행.
* API : lambda나 서버로 진행 시, 각 **단계의 결과 파일 확인 및 코드 세부 사항 확인** 어려울 것으로 판단되어 로컬에서 진행, es는 이미 RESTful하므로, flask를 이용하여 앞 단에 ES 접근 가능한 api를 생성
* 테스트의 편리함을 위해 하나의 웹페이지 생성.

##### 6. 소감
처음 해보는 것들이 많았다. 그래서 좋았다. 풀어야하는 과제로 생각하지 않았고, 자기개발의 기회로 삼아 밤을 새가며 머리를 싸맸다. 바보 같은 실수로 elasticsearch 관련하여 헤맬 때, stackoverflow에서 해결은 못해도 도움을 준 es tech evangelist 'dadoonet'에 감사한다. 더불어 이렇게 새롭고 다양한 경험을 하게 해주신 버즈니에 정말 감사하고, 많은 것을 배우는 계기가 되었다.

