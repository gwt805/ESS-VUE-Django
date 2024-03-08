FROM node:latest

LABEL name="ess-client-vue" auth="gwt"

RUN mkdir -p /app/client

WORKDIR /app/client

RUN npm config set -g registry https://registry.npmmirror.com/

COPY dist/ /app/client

COPY package.json /app/client/

RUN npm install

RUN echo "ess-client-vue build finished ..."