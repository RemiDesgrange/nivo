export default {
  mode: 'spa',
  /*
   ** Headers of the page
   */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || '',
      },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },
  /*
   ** Global CSS
   */
  css: [],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: ['@/plugins/highcharts',],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module',
  ],
  /*
   ** Nuxt.js modules
   */
  modules: ['bootstrap-vue/nuxt', '@nuxtjs/axios', '@nuxtjs/sentry'],
  /*
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {
      if (ctx.dev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/,
          options: {
            fix: true,
          },
        })
      }
    },
  },
  env: {
    baseUrl: `${process.env.API_PREFIX || 'http'}://${
      process.env.API_HOST || 'localhost'
    }:${process.env.API_PORT || 8000}`,
    ignBaseMapURL:
      process.env.IGN_BASE_MAP_URL ||
      'https://wxs.ign.fr/an7nvfzojv5wa96dsga5nk8w/geoportail/wmts',
  },
  axios: {
    progress: true,
  },
  bootstrapVue: {
    icons: true,
  },
  sentry: {
    config: {
      environment: process.env.ENV || 'production',
      release: process.env.COMMIT_REF || process.env.npm_package_version,
    },
    publishRelease: true,
  },
}
