export default {
  mode: 'universal',
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
        content: process.env.npm_package_description || ''
      }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
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
  plugins: [
    { src: '@/plugins/vuelayers', ssr: false } // ,
    // { src: '@/plugins/highcharts', ssr: false }
  ],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module'
  ],
  /*
   ** Nuxt.js modules
   */
  modules: [
    'bootstrap-vue/nuxt',
    '@/modules/vuelayers',
    '@nuxtjs/axios',
    'nuxt-fontawesome'
  ],
  /*
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {}
  },
  env: {
    baseUrl: `${process.env.API_PREFIX || 'http'}://${process.env.API_HOST ||
      'localhost'}:${process.env.API_PORT || 8000}`,
    baseMapUrl:
      process.env.BASE_MAP_URL ||
      'https://wxs.ign.fr/an7nvfzojv5wa96dsga5nk8w/geoportail/wmts'
  },
  axios: {
    progress: true
  },
  fontawesome: {
    imports: [
      {
        set: '@fortawesome/free-solid-svg-icons', // Solid icons
        icons: ['faTimes', 'faCheck']
      }
    ]
  }
}
