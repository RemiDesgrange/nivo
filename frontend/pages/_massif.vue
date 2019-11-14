<template>
  <app />
</template>

<script>
import App from '@/components/App'
import { alertTypes, mutationTypes as types } from '@/modules/stateTypes'

export default {
  components: {
    App
  },
  async asyncData({ store, params }) {
    await Promise.all([
      store.dispatch('fetchLastBraData'),
      store.dispatch('fetchNivoStation'),
      store.dispatch('fetchMassifs')
    ])
    const massifs = store.state.massifs.features.filter(
      (massif) => params.massif.toUpperCase() === massif.properties.name
    )
    if (massifs.length > 1 || massifs.length === 0) {
      store.commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: 'Massifs cannot be found'
      })
    } else {
      const selectedBra = store.state.braData.filter(
        (b) => b.massif.id === massifs[0].properties.id
      )
      store.commit(types.SET_SELECTED_BRA, selectedBra[0]) // ugly
    }
  }
}
</script>
