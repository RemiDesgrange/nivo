FROM node:11-alpine as builder

WORKDIR  /app
RUN chown node:node /app
USER node

COPY package-lock.json package.json /app/
RUN npm install

COPY . /app
RUN npm run build

ENV NODE_ENV=production
ENV HOST 0.0.0.0
EXPOSE 3000
CMD ["npm", "start"]