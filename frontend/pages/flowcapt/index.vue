<template>
  <div id="app">
    <navbar />
    <alert-manager />
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <chart :options="chartOptions"></chart>
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">{{ flowCaptData }}</div>
          <div class="w-100"></div>
          <div class="col"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { Chart } from 'highcharts-vue'

import Navbar from '@/components/Navbar'
import AlertManager from '@/components/alert/AlertManager'

export default {
  components: {
    Navbar,
    AlertManager,
    Chart
  },
  computed: {
    ...mapState(['flowCaptStations', 'flowCaptData']),
    chartOptions() {
      return {
        chart: {
          zoomType: 'x'
        },
        title: {
          text: 'test'
        },
        xAxis: {
          type: 'datetime'
        },
        series: Object.keys(this.flowCaptData.measures).map((fcKeys) => {
          return {
            type: 'area',
            name: fcKeys,
            data: this.flowCaptData.measures[fcKeys].map((e) => [e[1], e[0]])
          }
        })
      }
    }
  },
  async asyncData({ store }) {
    await store.dispatch('fetchFlowCaptStation')
    await store.dispatch('fetchFlowCaptData', 'FGIE1')
  }
}
</script>
