FROM node:18-slim

WORKDIR /app

COPY apps/frontend/package.json ./package.json

RUN npm install

COPY apps/frontend .

EXPOSE 3000

CMD ["node_modules/.bin/vite", "--host"]
