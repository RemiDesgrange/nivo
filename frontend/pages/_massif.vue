<template>
  <div id="app">
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <bra-data />
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <base-map>
              <bra-map />
            </base-map>
          </div>
          <div class="w-100"></div>
          <div class="col">
            <bra-chart />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseMap from '~/components/map/BaseMap'
import BraMap from '~/components/map/BraMap'
import BraData from '~/components/BraData'
import BraChart from '~/components/chart/BraChart'
import {
  alertTypes,
  globalMutationTypes as types,
  globalActionsTypes as actionsTypes,
  mapMutationTypes,
} from '~/modules/stateTypes'

export default {
  components: {
    BaseMap,
    BraMap,
    BraData,
    BraChart,
  },
  async asyncData({ store, params }) {
    // set map visibility
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'massifs',
      visibility: true,
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'flowcapt',
      visibility: false,
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'posteNivo',
      visibility: false,
    })
    // fetch massif
    await store.dispatch(actionsTypes.FETCH_MASSIFS)
    // select the fetched massif
    const massif = store.state.massifs.features.find(
      (massif) => params.massif.toUpperCase() === massif.properties.name
    )
    if (!massif) {
      store.commit(types.SET_ALERT, {
        level: alertTypes.DANGER,
        message: 'Massifs cannot be found',
      })
    } else {
      await store.dispatch(
        actionsTypes.FETCH_LAST_BRA_DATA,
        massif.properties.id
      )
      // const selectedBra = store.state.braData.find(
      //   (b) => b.massif.id === massif.properties.id
      // )
      // store.dispatch(actionsTypes.SET_SELECTED_BRA, selectedBra)
    }
  },
}
</script>
