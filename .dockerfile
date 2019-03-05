FROM ubuntu:18.04
MAINTAINER your_name "redrabbittt@naver.com"
RUN apt-get update -y
RUN apt-get install -y python3.7
COPY . /app
WORKDIR /app

RUN apt-get install python3-pip -y
#RUN pip3 install -r requirements.txt
RUN apt-get install default-jdk -y
RUN apt-get install openjdk-8-jre -y
RUN apt-get update
RUN wget -O - https://packages.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN echo  "deb  http://packages.elastic.co/elasticsearch/2.x/debian stable main" | tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
RUN apt-get update &&  apt-get install elasticsearch -y
ENTRYPOINT ["python"]

#CMD ["python driver.py"]
EXPOSE 9200
EXPOSE 5000
