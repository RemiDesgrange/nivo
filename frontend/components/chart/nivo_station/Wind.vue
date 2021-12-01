<template>
  <chart :options="chartWindOptions" />
</template>

<script>
import Highcharts from 'highcharts'
import WindbarbHighcharts from 'highcharts/modules/windbarb'

import NivoStationChartMixin from '~/components/chart/nivo_station/NivoStationChartMixin'
WindbarbHighcharts(Highcharts)

export default {
  mixins: [NivoStationChartMixin],
  computed: {
    chartWindOptions () {
      const measures = this.nivoData
      return {
        chart: {
          zoomType: 'x'
        },
        title: {
          text: 'Force et Direction du vent'
        },
        xAxis: {
          type: 'datetime',
          offset: 40
        },
        yAxis: {
          title: {
            text: 'Vitesse du vent (km/h'
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
          valueSuffix: '{point.x:%e. %b %H:%M:%Y}: {point.y:.2f} km/h'
        },
        series: [
          {
            data: measures.map((measure) => {
              return measure.ff * 3.6 // ms/s to km/h
            }),
            name: 'Vitesse du vent',
            keys: ['y'],
            type: 'area'
          }
          // {
          //   data: measures.map((measure, index) => {
          //     return [measure.ff, measures[index].dd]
          //   }),
          //   name: 'Vitesse du vent',
          //   keys: ['y', 'rotation'],
          //   type: 'area',
          // },
          // {
          //   data: measures.map((measure, index) => {
          //     return [measure.ff, measures[index].dd]
          //   }),
          //   name: 'Direction du vent',
          //   type: 'windbarb',
          // },
        ]
      }
    }
  }
}
</script>
