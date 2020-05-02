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
            <hr />
            <p>Ajouter ou enlever des données</p>
            <b-overlay :show="nivoDataLoading">
              <b-button-toolbar key-nav aria-label="Toolbar with button groups">
                <b-button-group class="mr-1">
                  <b-button
                    v-b-tooltip.hover
                    title="Enlever 30 jours"
                    @click="remove30days"
                    >--</b-button
                  >
                  <b-button
                    v-b-tooltip.hover
                    title="Enlever 1 jours"
                    @click="remove1day"
                    >-</b-button
                  >
                </b-button-group>
                <b-input-group class="mr1">
                  <b-form-input
                    :value="nivoStationDayLimit"
                    type="number"
                    @change="setDays"
                  />
                </b-input-group>
                <b-button-group class="mr-1">
                  <b-button
                    v-b-tooltip.hover
                    title="Ajouter 1 jours"
                    @click="add1day"
                    >+</b-button
                  >
                  <b-button
                    v-b-tooltip.hover
                    title="Ajouter 30 jours"
                    @click="add30days"
                    >++</b-button
                  >
                </b-button-group>
              </b-button-toolbar>
            </b-overlay>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import moment from 'moment'
import NivoDataChart from '~/components/chart/NivoDataChart'

import NivoMap from '~/components/map/NivoMap'
import BaseMap from '~/components/map/BaseMap'
import {
  globalActionsTypes as actionTypes,
  globalMutationTypes as types,
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
    ...mapState([
      'nivoData',
      'nivoStations',
      'selectedNivoStation',
      'nivoStationDayLimit',
      'nivoDataLoading',
    ]),
    ...mapGetters('map', [
      mapGettersTypes.SELECTED_NIVO_STATION_HOVER,
      mapGettersTypes.SELECTED_NIVO_STATION_CLICK,
    ]),
    lastData() {
      const lastDate = this.nivoData.slice().reverse().pop()
      if (lastDate) {
        return moment(lastDate.date).format('DD MM YYYY, hh:mm:ss')
      }
      return 'Inconnu'
    },
    altitudeStation() {
      return this.selectedNivoStation.geometry.coordinates[2]
    },
  },
  methods: {
    async setDays(val) {
      const nivoStationId = this.selectedNivoStation.properties.nss_id
      this.$store.commit(types.SET_NIVO_STATION_DAY_LIMIT, Number(val))
      const dayLimit = Number(val)
      await this.$store.dispatch('fetchNivoRecordsByStationIdWithDayLimit', {
        nivoStationId,
        dayLimit,
      })
    },
    async remove30days() {
      let rem = this.nivoStationDayLimit - 30
      if (rem < 1) {
        rem = 1
      }
      await this.setDays(rem)
    },
    async remove1day() {
      let rem = this.nivoStationDayLimit - 1
      if (rem < 1) {
        rem = 1
      }
      await this.setDays(rem)
    },
    async add1day() {
      await this.setDays(this.nivoStationDayLimit + 1)
    },
    async add30days() {
      await this.setDays(this.nivoStationDayLimit + 30)
    },
  },
}
</script>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>
