FROM node:8 as development

WORKDIR /app

COPY package.json /app

RUN npm install

COPY . /app
 
EXPOSE 4000

CMD ["node", "index.js"]
