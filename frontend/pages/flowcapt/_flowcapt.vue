<template>
  <div id="app">
    <navbar />
    <alert-manager />
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <chart :options="chartSnowLevelOptions"></chart>
          <!-- <chart :options="chartSnowDriftOptions"></chart> -->
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
    chartSnowLevelOptions() {
      return this.dataFor([
        { name: 'snow_height_seg1_nc', label: 'Snow Height Seg1' },
        { name: 'snow_height_seg2_nc', label: 'SnowHeight Seg2' }
      ])
    },
    chartSnowDriftOptions() {
      return this.dataFor([
        { name: 'snow_drift_seg1_flowcapt', label: 'Snow drift seg1' },
        { name: 'snow_drift_seg2_flowcapt', label: 'Snow drift seg2' }
      ])
    }
  },
  async asyncData({ store, params }) {
    await store.dispatch('fetchFlowCaptStation')
    await store.dispatch('fetchFlowCaptData', params.flowcapt)
  },
  methods: {
    dataFor(graphToFilter) {
      try {
        return {
          chart: {
            zoomType: 'x'
          },
          title: {
            text: 'graph'
          },
          xAxis: {
            type: 'date'
          },
          series: Object.keys(this.flowCaptData.measures)
            .filter((fcKeys) =>
              graphToFilter.map((e) => e.name).includes(fcKeys)
            )
            .map((fcKeys, index) => {
              return {
                type: 'area',
                name: graphToFilter[index].label,
                data: this.flowCaptData.measures[fcKeys].map((e) => [
                  e[1],
                  e[0]
                ])
              }
            })
        }
      } catch (e) {
        // alert !
      }
    }
  }
}
</script>
