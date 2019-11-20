<template>
  <div>
    <div v-if="flowCaptData">
      <client-only>
        <chart :highcharts="hcInstance" :options="chartSnowLevelOptions" />
        <chart :highcharts="hcInstance" :options="chartSnowDriftOptions" />
        <chart :highcharts="hcInstance" :options="chartWindDirOptions" />
        <chart :highcharts="hcInstance" :options="chartWindOptions" />
        <chart :highcharts="hcInstance" :options="chartAirTempOptions" />
        <chart :highcharts="hcInstance" :options="chartAirHumidityOptions" />
      </client-only>
    </div>
    <div v-if="flowCaptLoading">
      <div class="d-flex justify-content-center mb-3">
        <b-spinner style="width: 8rem; height: 8rem;" type="grow"></b-spinner>
      </div>
    </div>
  </div>
</template>

<script>
import Highcharts from 'highcharts'
import windbarbInit from 'highcharts/modules/windbarb'
import { Chart } from 'highcharts-vue'
import { mapState, mapMutations } from 'vuex'
import { mutationTypes as types, alertTypes } from '@/modules/stateTypes'

if (typeof Highcharts === 'object') {
  windbarbInit(Highcharts)
}

export default {
  components: {
    Chart
  },
  data() {
    return {
      hcInstance: Highcharts
    }
  },
  computed: {
    ...mapState(['flowCaptData', 'flowCaptLoading']),
    chartSnowLevelOptions() {
      return this.dataFor({
        title: {
          text: 'Hauteur de neige'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: {
            text: 'centimètre'
          }
        },
        plotOptions: {
          series: {
            marker: {
              radius: 0
            }
          }
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} m'
        },
        series: [
          {
            name: 'snow_height_seg1_nc',
            label: 'Hauteur Seg1'
          },
          {
            name: 'snow_height_seg2_nc',
            label: 'Hauteur Seg2'
          }
        ]
      })
    },
    chartSnowDriftOptions() {
      return this.dataFor({
        title: {
          text: 'Quantité de neige transporté par le vent'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: {
            text: 'g/m²/s'
          }
        },
        plotOptions: {
          series: {
            marker: {
              radius: 0
            }
          }
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} g/m²/s'
        },
        series: [
          {
            name: 'snow_drift_seg1_flowcapt',
            label: 'Snow drift seg1'
          },
          {
            name: 'snow_drift_seg2_flowcapt',
            label: 'Snow drift seg2'
          }
        ]
      })
    },
    chartWindDirOptions() {
      return this.dataFor({
        chart: {
          polar: true
        },
        title: {
          text: 'Direction du vent'
        },
        xAxis: {
          type: 'datetime'
        },
        plotOptions: {
          series: {
            marker: {
              radius: 0
            }
          }
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} °'
        },
        series: [
          {
            name: 'wind_direction_mini_young',
            label: 'Direction du vent mini'
            // type: 'windbarb'
          },
          {
            name: 'wind_direction_maxi_young',
            label: 'Direction du vent maxi'
            // type: 'windbarb'
          }
        ]
      })
    },
    chartWindOptions() {
      return this.dataFor({
        title: {
          text: 'Vent'
        },
        xAxis: {
          type: 'datetime'
        },
        plotOptions: {
          series: {
            marker: {
              radius: 0
            }
          }
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} km/h'
        },
        series: [
          {
            name: 'wind_speed_mean_flowcapt',
            label: 'Vitesse du vent moyenne'
          },
          {
            name: 'wind_speed_maxi_young',
            label: 'Vitesse du vent maxi'
          }
        ]
      })
    },
    chartAirTempOptions() {
      return this.dataFor({
        title: {
          text: 'Température Air'
        },
        xAxis: {
          type: 'datetime'
        },
        plotOptions: {
          series: {
            marker: {
              radius: 0
            }
          }
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} °C'
        },
        series: [
          {
            name: 'air_temperature_mean_nc',
            label: "Température de l'air"
          }
        ]
      })
    },
    chartAirHumidityOptions() {
      return this.dataFor({
        title: {
          text: 'Humidité air'
        },
        xAxis: {
          type: 'datetime'
        },
        plotOptions: {
          series: {
            marker: {
              radius: 0
            }
          }
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} %'
        },
        series: [
          {
            name: 'air_humidity_mean_nc',
            label: "Humidité de l'air"
          }
        ]
      })
    }
  },
  methods: {
    ...mapMutations([types.SET_ALERT]),
    dataFor(graphMetaData) {
      // Data need to be pre ordered, dunno with, seems to me that they are ordered :-/ highchart error 15
      try {
        graphMetaData.series = Object.keys(this.flowCaptData.measures)
          .filter((serie) =>
            graphMetaData.series.map((e) => e.name).includes(serie)
          )
          .map((serieKey, index) => {
            return {
              type: graphMetaData.series[index].type || 'area',
              name: graphMetaData.series[index].label,
              data: this.flowCaptData.measures[serieKey].map((e) => [
                e[1] * 1000,
                e[0]
              ])
            }
          })
        graphMetaData.chart = { zoomType: 'x' }
        return graphMetaData
      } catch (e) {
        this.$store.commit(types.SET_ALERT, {
          level: alertTypes.DANGER,
          message: 'Error drawing charts'
        })
      }
    }
  }
}
</script>
