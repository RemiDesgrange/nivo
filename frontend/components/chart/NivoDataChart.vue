<template>
  <div>
    <base-area-chart
      :point-start="lastData()"
      :series="chartSnowLevelOptions"
      title="Hauteur de neige"
    />
    <base-area-chart
      :point-start="lastData()"
      :series="chartWindOptions"
      title="Données vent"
    />
    <base-area-chart :options="chartAirTempOptions" />
    <div v-if="nivoDataLoading || nivoStationLoading">
      <div class="d-flex justify-content-center mb-3">
        <b-spinner style="width: 8rem; height: 8rem;" type="grow"></b-spinner>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'
import BaseAreaChart from '~/components/chart/BaseAreaChart'

export default {
  components: {
    BaseAreaChart,
  },
  computed: {
    ...mapState([
      'nivoData',
      'nivoStations',
      'selectedNivoStation',
      'nivoStationLoading',
      'nivoDataLoading',
    ]),
    chartSnowLevelOptions() {
      return [
        {
          type: 'area',
          name: 'Hauteur de neige',
          data: this.nivoData.map((n) => n.ht_neige * 100), // eslint-disable
        },
        {
          type: 'area',
          name: 'Hauteur de neige fraiche',
          data: this.nivoData.map((n) => n.ssfrai),
        },
      ]
    },
    chartWindOptions() {
      return [
        {
          type: 'area',
          name: 'Vitesse',
          data: this.nivoData.map((n) => n.ff),
        },
        {
          type: 'area',
          name: 'Direction',
          data: this.nivoData.map((n) => n.dd),
        },
      ]
    },
    chartAirTempOptions() {
      return [
        {
          name: 'Humidité',
          data: this.nivoData.map((n) => n.u),
        },
        {
          name: 'Température',
          data: this.nivoData.map((n) => n.t + 273.15),
        },
        {
          name: 'Point de rosé',
          data: this.nivoData.map((n) => n.td + 273.15),
        },
      ]
    },
  },
  methods: {
    lastData() {
      const lastData = this.nivoData
        .map((n) => moment(n.date))
        .sort()
        .reverse()
      if (lastData.length > 0) {
        return lastData[0].utc().valueOf()
      }
      return moment().utc().valueOf()
    },
  },
}
</script>
