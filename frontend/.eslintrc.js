module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended'
  ],
  plugins: [],
  // add your custom rules here
  rules: {
  },
  overrides: [
    {
      files: ['components/**/*.vue', 'pages/**/*.vue'],
      rules: { 'vue/multi-word-component-names': 'off' }
    }
  ]
}
