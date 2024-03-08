FROM python:3.8

LABEL name="ess-server-django" auth="gwt"

RUN mkdir -p /app/server

WORKDIR /app/server

COPY . /app/server

RUN apt-get update && apt-get install -y libgl1

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

RUN echo "ess-server-django build finished ..."