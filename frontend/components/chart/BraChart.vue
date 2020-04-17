<template>
  <div>
    <div v-if="braData">
      <chart
        v-if="riskEvolution"
        :options="riskSerie"
        title="Evolution du risque"
      />
      <base-area-chart
        v-if="iso0Evolution && isoMinus10Evolution"
        :series="isoSerie"
        title="Evolution iso"
        y-axis-text="Altitude"
      />
      <base-area-chart
        v-if="snowLimitNorth && snowLimitSouth"
        :series="snowLimitSerie"
        title="Evolution hauteur limite de neige"
        y-axis-text="Altitude"
      />
      <div v-if="loadingData && braLoading">
        <div class="d-flex justify-content-center mb-3">
          <b-spinner style="width: 8rem; height: 8rem;" type="grow"></b-spinner>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'
import { Chart } from 'highcharts-vue'
import { globalMutationTypes as types } from '~/modules/stateTypes'
import BaseAreaChart from '~/components/chart/BaseAreaChart'

export default {
  components: {
    BaseAreaChart,
    Chart,
  },
  data() {
    return {
      records: null,
      riskEvolution: null,
      windEvolution: null,
      iso0Evolution: null,
      isoMinus10Evolution: null,
      snowLimitNorth: null,
      snowLimitSouth: null,
      loadingData: true,
    }
  },
  computed: {
    ...mapState(['braData', 'braLoading']),
    riskSerie() {
      return {
        chart: {
          zoomType: 'x',
        },
        title: {
          text: 'Evolution du risque',
        },
        xAxis: {
          type: 'datetime',
        },
        yAxis: {
          title: {
            text: 'Risque',
          },
          allowDecimals: false,
          min: 1,
        },
        plotOptions: {
          area: {
            fillColor: {
              linearGradient: [0, 0, 0, 300],
              stops: [
                [0, 'rgba(254, 5, 0, 1)'],
                [0.25, 'rgba(254, 35, 32, 1)'],
                [0.5, 'rgba(255, 158, 1, 1)'],
                [0.75, 'rgba(254, 255, 0, 1)'],
                [1, 'rgba(205, 255, 96, 1)'],
              ],
            },
            marker: {
              radius: 2,
            },
            lineWidth: 0,
            states: {
              hover: {
                lineWidth: 0,
              },
            },
            threshold: null,
          },
        },
        series: [
          {
            type: 'area',
            data: this.riskEvolution,
            name: 'risque',
          },
        ],
      }
    },
    isoSerie() {
      return [
        {
          data: this.iso0Evolution,
          name: 'iso 0',
        },
        {
          data: this.isoMinus10Evolution,
          name: 'iso moins 10',
        },
      ]
    },
    snowLimitSerie() {
      return [
        {
          name: 'Limite hauteur de neige nord',
          data: this.snowLimitNorth,
        },
        {
          name: 'Limite hauteur de neige sud',
          data: this.snowLimitSouth,
        },
      ]
    },
    startDate() {
      const lastData = this.records
        .map((n) => moment(n.production_date))
        .sort()
        .reverse()
      if (lastData.length > 0) {
        return lastData[0].utc().valueOf()
      }
      return moment().utc().valueOf()
    },
  },
  async mounted() {
    this.loadingData = true
    const massif = this.braData.massif.id
    try {
      const recordsRequest = await this.$axios.get(
        `${process.env.baseUrl}/bra/massifs/${massif}/records`
      )
      this.records = recordsRequest.data
      this.records.sort(
        (a, b) => moment(a.production_date) - moment(b.production_date)
      )

      this.riskEvolution = this.records.map((e) => ({
        x: moment(e.production_date).toDate(),
        y: e.max_risk,
      }))
      this.iso0Evolution = this.records.flatMap((r) => {
        return r.weather_forcasts.map((wf) => ({
          x: moment(wf.expected_date).toDate(),
          y: wf.iso0,
        }))
      })
      this.isoMinus10Evolution = this.records.flatMap((r) => {
        return r.weather_forcasts.map((wf) => ({
          x: moment(wf.expected_date).toDate(),
          y: wf.iso_minus_10,
        }))
      })
      this.snowLimitNorth = this.records.map((e) => ({
        y: e.snowlimit_north,
        x: moment(e.production_date).toDate(),
      }))
      this.snowLimitSouth = this.records.map((e) => ({
        y: e.snowlimit_south,
        x: moment(e.production_date).toDate(),
      }))
    } catch (ex) {
      this.$store.commit(types.SET_ALERT, {
        message: 'Cannot downloads BRA datas',
        level: 'danger',
      })
    }
    this.loadingData = false
  },
}
</script>
