<template>
  <app />
</template>

<script>
import App from '@/components/App'

export default {
  components: {
    App
  },
  async asyncData({ store }) {
    console.log('Trying to load')
    await Promise.all([
      store.dispatch('fetchMassifs'),
      store.dispatch('fetchNivoStation')
    ])
  }
}
</script>
