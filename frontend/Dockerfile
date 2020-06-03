FROM node:lts-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install -g @vue/cli \
 && npm install

CMD [ "npm", "run", "serve" ]
