<template>
  <app />
</template>

<script>
import App from '@/components/App'
import { alertTypes } from '@/modules/stateTypes'

export default {
  components: {
    App
  },
  async asyncData({ store, params }) {
    await store.dispatch('fetchMassifs')
    await store.dispatch('fetchNivoseStation')
    const massifs = store.state.massifs.features.filter(
      (massif) => params.massif.toUpperCase() === massif.properties.name
    )
    if (massifs.length > 1 || massifs.length === 0) {
      store.commit('SET_ALERT', alertTypes.DANGER, 'Massifs cannot be found')
    } else {
      await store.dispatch('fetchLastBraById', massifs[0].properties.id)
    }
  }
}
</script>
