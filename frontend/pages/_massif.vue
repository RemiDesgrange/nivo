<template>
  <div id="app">
    <navbar />
    <alert-manager />
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
          <div class="col">
            <nivo-data />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseMap from '@/components/map/BaseMap'
import Navbar from '@/components/Navbar'
import BraData from '@/components/BraData'
import NivoData from '@/components/NivoData'
import AlertManager from '@/components/alert/AlertManager'
import { alertTypes, mutationTypes as types } from '@/modules/stateTypes'

export default {
  components: {
    Navbar,
    BaseMap,
    BraData,
    NivoData,
    AlertManager
  },
  async asyncData({ store, params }) {
    await Promise.all([
      store.dispatch('fetchLastBraData'),
      store.dispatch('fetchNivoStation'),
      store.dispatch('fetchMassifs')
    ])
    const massif = store.state.massifs.features.find(
      (massif) => params.massif.toUpperCase() === massif.properties.name
    )

    if (!massif) {
      store.commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: 'Massifs cannot be found'
      })
    } else {
      const selectedBra = store.state.braData.find(
        (b) => b.massif.id === massif.properties.id
      )
      store.commit(types.SET_SELECTED_BRA, selectedBra)
    }
  }
}
</script>
