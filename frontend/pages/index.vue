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
    // in order to populate massifs color, we need the risk of all the bra.
    // await store.dispatch('fetchLastBraRiskLevel')
  }
}
</script>
