FROM node:16 as development

WORKDIR /app

COPY package*.json /app

RUN npm install

COPY . /app
 
EXPOSE 8000

CMD ["node", "index.js"]
