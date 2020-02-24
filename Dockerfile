# base image
# FROM python:3.7
FROM ubuntu:18.04
# a little overkill but need it to install dot cli for dtreeviz

# update ubuntu
# https://stackoverflow.com/questions/45142855/bin-sh-apt-get-not-found
RUN apt-get update

# install python and pip
RUN apt-get install python3.7 -y
RUN apt-get install python3-pip -y

# installing graphviz so dtreeviz package works
RUN apt-get install graphviz -y

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


# exposing default port for streamlit
EXPOSE 8501

# copy over requirements
COPY requirements.txt ./requirements.txt

# install pip then packages
# RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# copying all files over
COPY . .


# run app
CMD streamlit run app.py