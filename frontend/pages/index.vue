<template>
  <div id="app">
    <b-container fluid>
      <b-row>
        <b-col lg="6" md="12" sm="12">
          <bra-data />
        </b-col>
        <b-col lg="6" md="12" sm="12">
          <b-col>
            <base-map>
              <bra-map />
            </base-map>
          </b-col>
          <div class="w-100" />
          <b-col>
            <bra-chart v-if="braData" />
          </b-col>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex'
import BaseMap from '~/components/map/BaseMap'
import BraMap from '~/components/map/BraMap'
import BraData from '~/components/BraData'
import BraChart from '~/components/chart/BraChart'
import {
  globalActionsTypes as actionsTypes,
  mapMutationTypes,
  mapGettersTypes
} from '~/modules/stateTypes'

export default {
  components: {
    BaseMap,
    BraMap,
    BraData,
    BraChart
  },
  async asyncData ({ store, params }) {
    // fetch massif
    await store.dispatch(actionsTypes.FETCH_MASSIFS)
  },
  methods: {
    ...mapMutations('map', [mapMutationTypes.SET_VISIBILITY])
  },
  computed: {
    ...mapState(['braData']),
    ...mapGetters('map', [mapGettersTypes.SELECTED_MASSIF_CLICK]),
    selectedMassif () {
      return this.SELECTED_MASSIF_CLICK
    }
  },
  mounted () {
    // set map visibility
    this.SET_VISIBILITY({
      layerName: 'massifs',
      visibility: true
    })
    this.SET_VISIBILITY({
      layerName: 'flowcapt',
      visibility: false
    })
    this.SET_VISIBILITY({
      layerName: 'posteNivo',
      visibility: false
    })
  }
}
</script>
