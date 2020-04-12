<template>
  <div id="app">
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <bra-data />
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <base-map />
          </div>
          <div class="w-100"></div>
          <div class="col"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseMap from '~/components/map/BaseMap'
import BraData from '~/components/BraData'
import { alertTypes, gloablMutationTypes as types } from '~/modules/stateTypes'

export default {
  components: {
    BaseMap,
    BraData,
  },
  async asyncData({ store, params }) {
    await Promise.all([
      store.dispatch('fetchLastBraData'),
      store.dispatch('fetchMassifs'),
    ])
    const massif = store.state.massifs.features.find(
      (massif) => params.massif.toUpperCase() === massif.properties.name
    )

    if (!massif) {
      store.commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: 'Massifs cannot be found',
      })
    } else {
      const selectedBra = store.state.braData.find(
        (b) => b.massif.id === massif.properties.id
      )
      store.commit(types.SET_SELECTED_BRA, selectedBra)
    }
  },
}
</script>
