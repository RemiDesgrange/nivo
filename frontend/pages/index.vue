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
            <!--            <nivo-data />-->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  globalActionsTypes as actionsTypes,
  mapMutationTypes,
} from '~/modules/stateTypes'

import BaseMap from '~/components/map/BaseMap'
import BraMap from '~/components/map/BraMap'
import BraData from '~/components/BraData'

export default {
  components: {
    BaseMap,
    BraData,
    BraMap,
  },
  async asyncData({ store }) {
    await store.dispatch(actionsTypes.FETCH_MASSIFS)
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
  },
}
</script>
