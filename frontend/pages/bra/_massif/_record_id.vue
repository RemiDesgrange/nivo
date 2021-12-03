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
import { mapGetters, mapState } from 'vuex'
import BaseMap from '~/components/map/BaseMap'
import BraMap from '~/components/map/BraMap'
import BraData from '~/components/BraData'
import BraChart from '~/components/chart/BraChart'
import {
  alertTypes,
  globalMutationTypes as types,
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
    // set map visibility
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'massifs',
      visibility: true
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'flowcapt',
      visibility: false
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'posteNivo',
      visibility: false
    })
    // fetch massif
    await store.dispatch(actionsTypes.FETCH_MASSIFS)
    // select the fetched massif
    if (params.massif !== undefined && params.record_id !== undefined) {
      const massif = store.state.massifs.features.find(
        massif => params.massif.toUpperCase() === massif.properties.name
      )
      const recordId = params.record_id
      if (!massif && !recordId) {
        store.commit(types.SET_ALERT, {
          level: alertTypes.DANGER,
          message: 'Massifs for that date cannot be found'
        })
      } else {
        await store.dispatch(actionsTypes.FETCH_BRA_DATA, recordId)
      }
    }
  },
  computed: {
    ...mapState(['braData']),
    ...mapGetters('map', [mapGettersTypes.SELECTED_MASSIF_CLICK]),
    selectedMassif () {
      return this.SELECTED_MASSIF_CLICK
    }
  },
  watch: {
    selectedMassif (newMassif) {
      if (newMassif.length > 0) {
        this.$router.push(`/bra/${newMassif[0].get('name').toLowerCase()}`)
      } else {
        this.$router.push('/')
      }
    }
  }
}
</script>
