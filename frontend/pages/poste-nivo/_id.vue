<template>
  <div id="app">
    <navbar />
    <alert-manager />
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
            <!-- <dl v-if="selectedStation">
              <dt>Station</dt>
              <dd>{{ selectedStation.properties.fcs_id }}</dd>
              <dt>label</dt>
              <dd>{{ selectedStation.properties.fcs_site }}</dd>
              <dt>pays</dt>
              <dd>{{ selectedStation.properties.fcs_country }}</dd>
              <dt>Dernier relevé</dt>
              <dd v-if="oldLastData(flowCaptData.lastdata)">
                {{ flowCaptData.lastdata }}
                <font-awesome-icon
                  id="lastDataIndicatorKo"
                  :style="{ color: 'red' }"
                  icon="times"
                />
              </dd>
              <dd v-else>
                {{ flowCaptData.lastdata }}
                <font-awesome-icon
                  id="lastDataIndicatorOk"
                  :style="{ color: 'green' }"
                  icon="check"
                />
              </dd>
            </dl>
            <b-tooltip target="lastDataIndicatorOk" placement="right">
              The capteur send his data at {{ flowCaptData.lastdata }}
            </b-tooltip>
            <b-tooltip target="lastDataIndicatorKo" placement="right">
              The capteur send his data more than 1 days ago at
              {{ flowCaptData.lastdata }}
            </b-tooltip> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'
import NivoDataChart from '@/components/chart/NivoDataChart'

import Navbar from '@/components/Navbar'
import NivoMap from '@/components/map/NivoMap'
import BaseMap from '@/components/map/BaseMap'
import AlertManager from '@/components/alert/AlertManager'
import { mutationTypes as types } from '@/modules/stateTypes'

export default {
  components: {
    Navbar,
    AlertManager,
    NivoMap,
    NivoDataChart,
    BaseMap
  },
  computed: {
    ...mapState(['nivoData', 'nivoStations', 'selectedNivoStation']),
    selectedStation() {
      if (this.nivoData && this.nivoStations) {
        return this.nivoStations.features.find(
          (f) => this.nivoData.station === f.properties.nss_id
        )
      } else {
        return null
      }
    }
  },
  async asyncData({ store, params }) {
    await store.dispatch('fetchNivoStation').then(() => {
      store.commit(
        types.SET_SELECTED_NIVO_STATION,
        store.state.nivoStations.features.find(
          (s) => s.properties.nss_id === params.id
        )
      )
    })
    await store.dispatch('fetchNivoRecordsByStationId', params.id)
  },
  methods: {
    oldLastData(dateAsStr) {
      return moment().diff(moment(dateAsStr), 'days') > 1
    }
  },
  filters: {
    cleanStationsName(station) {
      return station.toLowerCase().replace('_', ' ')
    }
  }
}
</script>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>
