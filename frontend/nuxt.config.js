export default {
  ssr: false,
  /*
   ** Headers of the page
   */
  head: {
    title: 'Nivo',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '96x96',
        href: '/favicon-96x96.png'
      },
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '32x32',
        href: '/favicon-32x32.png'
      },
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '16x16',
        href: '/favicon-16x16.png'
      }
    ]
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },
  loadingIndicator: { name: 'pulse', color: '#000', background: '#dbdbdb' },
  /*
   ** Global CSS
   */
  css: [],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [{ src: '@/plugins/map-plugin', ssr: false }],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module',
    '@nuxtjs/moment'
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
    extend (config, ctx) {
      if (ctx.dev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/,
          options: {
            fix: true
          }
        })
      }
    }
  },
  env: {
    baseUrl: `${process.env.API_PREFIX || 'http'}://${
      process.env.API_HOST || 'localhost'
    }:${process.env.API_PORT || 9000}`,
    ignBaseMapURL:
      process.env.IGN_BASE_MAP_URL ||
      'https://wxs.ign.fr/an7nvfzojv5wa96dsga5nk8w/geoportail/wmts'
  },
  axios: {
    progress: true
  },
  bootstrapVue: {
    icons: false,
    directivePlugins: ['VBTooltipPlugin', 'VBTogglePlugin'],
    components: [
      'BContainer',
      'BCol',
      'BRow',
      'BFormGroup',
      'BFormCheckbox',
      'BFormInput',
      'BFormRadio',
      'BFormRadioGroup',
      'BNavbar',
      'BNavbarBrand',
      'BCollapse',
      'BNavbarNav',
      'BNavItem',
      'BJumbotron',
      'BButton',
      'BCard',
      'BCardTitle',
      'BCardText',
      'BCardBody',
      'BButtonGroup',
      'BButtonToolbar',
      'BInputGroup',
      'BEmbed',
      'BLink',
      'BSpinner',
      'BTooltip',
      'BOverlay',
      'BIconLayers',
      'BIconX',
      'BIconCheck',
      'BIconGithub',
      'BProgress',
      'BAlert'
    ]
  },
  sentry: {
    config: {
      environment: process.env.ENV || 'production',
      release: process.env.COMMIT_REF || process.env.npm_package_version
    },
    publishRelease: true,
    disabled: process.env.SENTRY_DISABLED !== 'false'
  },
  moment: {
    defaultLocale: 'fr',
    locales: ['fr']
  }
}
