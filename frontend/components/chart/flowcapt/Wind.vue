<template>
  <chart :options="chartWindOptions" />
</template>

<script>
import Highcharts from 'highcharts'
import WindbarbHighcharts from 'highcharts/modules/windbarb'

import FlowCaptChartMixin from '~/components/chart/flowcapt/FlowCaptChartMixin'
WindbarbHighcharts(Highcharts)

export default {
  mixins: [FlowCaptChartMixin],
  computed: {
    chartWindOptions () {
      const measures = this.flowCaptData.measures
      return {
        title: {
          text: 'Force et Direction du vent'
        },
        xAxis: {
          type: 'datetime',
          offset: 40
        },
        yAxis: {
          title: {
            text: 'Vitesse du vent'
          }
        },
        plotOptions: {
          series: {
            pointStart: this.lastData,
            pointInterval: 3600 * 1000, // 1h
            marker: {
              radius: 0
            }
          }
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          valueSuffix: ' km/h'
        },
        series: [
          {
            data: measures.wind_speed_maxi_young.map((measure, index) => {
              return [measure, measures.wind_direction_maxi_young[index]]
            }),
            name: 'Vitesse du vent maxi',
            keys: ['y', 'rotation'],
            type: 'area'
          },
          {
            data: measures.wind_speed_maxi_young.map((measure, index) => {
              return [measure, measures.wind_direction_maxi_young[index]]
            }),
            name: 'Direction du vent maxi',
            type: 'windbarb'
          }
        ]
      }
    }
  }
}
</script>
