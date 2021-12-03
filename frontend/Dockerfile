FROM node:16-slim

RUN apt update && apt install ca-certificated && rm -rf /var/lib/apt/lists/*

ARG SENTRY_DSN
ARG SENTRY_DISABLED
ARG SENTRY_ORG
ARG SENTRY_PROJECT
ARG SENTRY_AUTH_TOKEN
ARG API_HOST
ARG API_PREFIX
ARG API_PORT
ENV NODE_ENV=build \
  SENTRY_DSN=${SENTRY_DSN}\
  SENTRY_DISABLED=${SENTRY_DISABLED}\
  SENTRY_ORG=${ ENTRY_ORG}\
  SENTRY_PROJECT=${SENTRY_PROJECT}
  SENTRY_AUTH_TOKEN=${SENTRY_AUTH_TOKEN}
  API_HOST=${API_HOST} API_PREFIX=${API_PREFIX} API_PORT=${API_PORT}
WORKDIR /app
RUN chown node:node /app

USER node
COPY --chown=node:node package.json package-lock.json /app/
RUN npm install

ENV NODE_ENV=production
ENV HOST 0.0.0.0
COPY --chown=node:node . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "start"]
