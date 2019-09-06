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
    await Promise.all([
      store.dispatch('fetchMassifs'),
      store.dispatch('fetchNivoStation')
    ])
  }
}
</script>
