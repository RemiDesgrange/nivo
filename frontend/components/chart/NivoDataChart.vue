<template>
  <div>
    <b-overlay :show="show">
      <snow />
    </b-overlay>
    <b-overlay :show="show">
      <wind />
    </b-overlay>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'
import Wind from '~/components/chart/nivo_station/Wind'
import Snow from '~/components/chart/nivo_station/Snow'

export default {
  components: {
    Wind,
    Snow,
  },
  computed: {
    show() {
      return this.nivoDataLoading || this.nivoStationLoading
    },
    ...mapState([
      'nivoData',
      'nivoStations',
      'selectedNivoStation',
      'nivoStationLoading',
      'nivoDataLoading',
    ]),
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
        .pop()
      return lastData.utc().valueOf()
    },
  },
}
</script>
