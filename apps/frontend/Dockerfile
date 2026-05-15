FROM node:20-slim

WORKDIR /app

COPY apps/frontend/package.json ./package.json

RUN npm install

COPY apps/frontend .

EXPOSE 3000

CMD ["node_modules/.bin/vite", "--host", "--port", "3000"]
