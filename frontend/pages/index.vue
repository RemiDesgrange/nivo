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
    await store.dispatch('fetchMassifs')
    await store.dispatch('fetchNivoseStation')
  }
}
</script>
