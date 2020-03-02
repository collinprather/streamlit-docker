# base image
# FROM python:3.7
FROM ubuntu:18.04
# a little overkill but need it to install dot cli for dtreeviz

# update ubuntu
# https://stackoverflow.com/questions/45142855/bin-sh-apt-get-not-found
# install python and pip
# installing graphviz so dtreeviz package works
# install nano in case I need it
# need to install psycopg2
RUN apt-get update &&\
    apt-get install python3.7 -y &&\
    apt-get install python3-pip -y &&\
    apt-get install graphviz -y &&\
    apt-get install nano -y &&\
    apt-get install libpq-dev -y

# exposing default port for streamlit
EXPOSE 8501

# making directory of app
WORKDIR /streamlit-docker

# copy over requirements
COPY requirements.txt ./requirements.txt

# installing required packages
RUN pip3 install -r requirements.txt

# copying all app files to image
COPY . .

# cmd to launch app when container is run
CMD python3 scripts/load_docker_db.py
CMD streamlit run app.py

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'
