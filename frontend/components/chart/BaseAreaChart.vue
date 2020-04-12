<template>
  <client-only>
    <chart :options="chartOptions" />
  </client-only>
</template>

<script>
import { Chart } from 'highcharts-vue'
import moment from 'moment'

export default {
  components: {
    Chart,
  },
  props: {
    title: {
      type: String,
      default: 'Inconnu',
    },
    yAxisText: { type: String, default: 'Inconnu' },
    pointStart: {
      type: Number,
      default: moment().utc().valueOf(),
    },
    pointInterval: { type: Number, default: 3600 * 1000 },
    tooltip: {
      type: Object,
      default() {
        return {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} m',
        }
      },
    },
    series: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chartOptions: {
        chart: {
          zoomType: 'x',
        },
        title: {
          text: this.title,
        },
        xAxis: {
          type: 'datetime',
        },
        yAxis: {
          title: {
            text: this.yAxisText,
          },
        },
        plotOptions: {
          series: {
            pointStart: this.pointStart,
            pointInterval: this.pointInterval,
            marker: {
              radius: 0,
            },
          },
        },
        tooltip: this.tooltip,
        series: this.series,
      },
    }
  },
}
</script>
