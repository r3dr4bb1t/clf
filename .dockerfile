FROM ubuntu:18.04
MAINTAINER your_name "redrabbittt@naver.com"
RUN apt-get update -y
RUN apt-get install -y python3.7
COPY . /app
WORKDIR /app
RUN apt-get install python3-pip -y
RUN pip3 install -r ./categorization/requirements.txt
RUN apt-get install default-jdk -y
RUN apt-get install openjdk-8-jre -y
RUN apt-get install wget -y
RUN apt-get update

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN apt-get install apt-transport-https
RUN echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-5.x.list
RUN apt-get update &&  apt-get install elasticsearch -y
#RUN apt-get install systemd
#RUN systemctl service elasticsearch start
RUN service elasticsearch start
#CMD ["python3 /categorization/driver.py"]
EXPOSE 9200
EXPOSE 5000
