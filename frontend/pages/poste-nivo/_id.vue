<template>
  <div id="app">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <h1 class="capitalize">
            Station
            {{ selectedNivoStation.properties.nss_name | cleanStationsName }}
          </h1>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <nivo-data-chart />
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <base-map>
              <nivo-map />
            </base-map>
          </div>
          <div class="w-100"></div>
          <div class="col">
            <dl v-if="selectedNivoStation">
              <dt>Station</dt>
              <dd class="capitalize">
                {{
                  selectedNivoStation.properties.nss_name | cleanStationsName
                }}
              </dd>
              <dt>Dernier relevé</dt>
              <dd>{{ lastData }}</dd>
              <dt>Altitude Station</dt>
              <dd>{{ altitudeStation }}</dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'
import NivoDataChart from '~/components/chart/NivoDataChart'

import NivoMap from '~/components/map/NivoMap'
import BaseMap from '~/components/map/BaseMap'
import {
  globalActionsTypes as actionTypes,
  // globalMutationTypes as types,
  mapGettersTypes,
  mapMutationTypes,
} from '@/modules/stateTypes'

export default {
  components: {
    NivoMap,
    NivoDataChart,
    BaseMap,
  },
  filters: {
    cleanStationsName(station) {
      return station.toLowerCase().replace('_', ' ')
    },
  },
  async asyncData({ store, params }) {
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'massifs',
      visibility: false,
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'flowcapt',
      visibility: false,
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'posteNivo',
      visibility: true,
    })
    await store.dispatch(actionTypes.FETCH_NIVO_STATIONS)
    await store.dispatch('fetchNivoRecordsByStationId', params.id)
    store.dispatch(
      actionTypes.SET_SELECTED_NIVO_STATION,
      store.state.nivoStations.features.find(
        (s) => s.properties.nss_id === params.id
      )
    )
  },
  computed: {
    ...mapState(['nivoData', 'nivoStations', 'selectedNivoStation']),
    ...mapState('map', [
      mapGettersTypes.SELECTED_NIVO_STATION_HOVER,
      mapGettersTypes.SELECTED_NIVO_STATION_CLICK,
    ]),
    lastData() {
      const lastData = this.nivoData
        .map((n) => moment(n.date))
        .sort()
        .reverse()
      if (lastData.length > 0) {
        return lastData[0].format('DD MM YYYY, hh:mm:ss')
      }
      return 'Inconnu'
    },
    altitudeStation() {
      return this.selectedNivoStation.geometry.coordinates[2]
    },
  },
}
</script>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>
