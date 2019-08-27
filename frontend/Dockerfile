FROM node:10-alpine as builder

USER node

COPY --chown=node:node package.json package-lock.json /app/
WORKDIR /app
RUN npm install
COPY . /app
RUN npm run build


FROM nginx:1.17

COPY --from=build --chown=www-data /app/dist /usr/share/nginx/html



