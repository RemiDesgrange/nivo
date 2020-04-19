<template>
  <chart :options="chartOptions" />
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
    yAxisLabel: { type: String, default: '{value} m' },
    pointStart: {
      type: Number,
      default: moment().utc().valueOf(),
    },
    pointInterval: { type: Number, default: 3600 * 1000 }, // in milliseconds !!
    pointIntervalUnit: {
      type: String,
      default: undefined,
    },
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
          labels: {
            format: this.yAxisLabel,
          },
        },
        plotOptions: {
          series: {
            pointStart: this.pointStart,
            pointInterval: this.pointInterval,
            pointIntervalUnit: this.pointIntervalUnit,
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
