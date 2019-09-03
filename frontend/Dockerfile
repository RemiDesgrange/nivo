FROM node:slim

ENV NODE_ENV=build
WORKDIR /app
RUN chown node:node /app

USER node
COPY package.json package-lock.json ./
RUN npm install

ENV NODE_ENV=production
ENV HOST 0.0.0.0
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "start"]
