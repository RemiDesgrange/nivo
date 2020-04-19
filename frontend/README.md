# Nivo Frontend

This is the frontend of Nivo. This app is build with nuxtjs in `universal` mode. This mean you need a nodejs server to serve the HTML/CSS/JS files.

Dockerfile is meant for production build.

## Build Setup

``` bash
# install dependencies
$ npm run install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).

## Sentry setup

When [sentry](https://sentry.io) is used. `npm run build` will send the release to sentry.

In order to do it properly you need several environment variables :

* `SENTRY_DSN`: find in the sentry project settings
* `SENTRY_PROJECT`: your project slug
* `SENTRY_ORG`: your org slug
* `SENTRY_AUTH_TOKEN`: you need to create a token [here](https://sentry.io/settings/account/api/auth-tokens/) and then fill it.


