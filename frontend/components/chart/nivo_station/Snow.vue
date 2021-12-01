<template>
  <chart :options="chartSnowOptions" />
</template>

<script>
import moment from 'moment'
import NivoStationChartMixin from '~/components/chart/nivo_station/NivoStationChartMixin'

export default {
  mixins: [NivoStationChartMixin],
  computed: {
    chartSnowOptions () {
      const sortedMeasure = this.nivoData
        .slice()
        .sort((a, b) => moment(a.date) - moment(b.date))
      return {
        chart: {
          zoomType: 'x'
        },
        title: {
          text: 'Hauteur de neige'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: {
            text: 'Hauteur (cm)'
          }
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M:%Y}: {point.y:.2f} cm'
        },
        series: [
          {
            type: 'area',
            name: 'Hauteur de neige',
            data: sortedMeasure.map(n => [
              moment(n.date).utc().valueOf(),
              n.ht_neige * 100
            ])
          },
          {
            type: 'area',
            name: 'Hauteur de neige fraiche',
            data: sortedMeasure.map(n => [
              moment(n.date).utc().valueOf(),
              n.ssfrai
            ])
          }
        ]
      }
    }
  }
}
</script>
