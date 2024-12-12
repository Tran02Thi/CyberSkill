FROM node:8 as development
WORKDIR /app  
COPY package*.json /app
RUN npm install --legacy-peer-deps  
COPY . /app  
EXPOSE 8081  
CMD ["node", "index.js"]