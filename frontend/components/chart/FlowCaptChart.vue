<template>
  <div>
    <div v-if="flowCaptData">
      <client-only>
        <chart :options="chartSnowLevelOptions" />
        <chart :options="chartSnowDriftOptions" />
        <chart :options="chartWindOptions" />
        <chart :options="chartAirTempOptions" />
        <chart :options="chartAirHumidityOptions" />
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
import { Chart } from 'highcharts-vue'
import { mapState } from 'vuex'
import moment from 'moment'
import { globalMutationTypes as types, alertTypes } from '~/modules/stateTypes'

export default {
  components: {
    Chart,
  },
  computed: {
    ...mapState(['flowCaptData', 'flowCaptLoading']),
    chartSnowLevelOptions() {
      return this.dataFor({
        title: {
          text: 'Hauteur de neige',
        },
        xAxis: {
          type: 'datetime',
        },
        yAxis: {
          title: {
            text: 'centimètre',
          },
        },
        plotOptions: {
          series: {
            pointStart: moment(this.flowCaptData.lastdata).utc().valueOf(),
            pointInterval: 3600 * 1000, // 1h
            marker: {
              radius: 0,
            },
          },
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} m',
        },
        series: [
          {
            name: 'snow_height_seg1_nc',
            label: 'Hauteur Seg1',
          },
          {
            name: 'snow_height_seg2_nc',
            label: 'Hauteur Seg2',
          },
        ],
      })
    },
    chartSnowDriftOptions() {
      return this.dataFor({
        title: {
          text: 'Quantité de neige transporté par le vent',
        },
        xAxis: {
          type: 'datetime',
        },
        yAxis: {
          title: {
            text: 'g/m²/s',
          },
        },
        plotOptions: {
          series: {
            marker: {
              radius: 0,
            },
          },
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} g/m²/s',
        },
        series: [
          {
            name: 'snow_drift_seg1_flowcapt',
            label: 'Snow drift seg1',
          },
          {
            name: 'snow_drift_seg2_flowcapt',
            label: 'Snow drift seg2',
          },
        ],
      })
    },
    chartWindOptions() {
      return this.dataForWind({
        title: {
          text: 'Force et Direction du vent',
        },
        xAxis: {
          type: 'datetime',
          offset: 40,
        },
        plotOptions: {
          series: {
            pointStart: moment(this.flowCaptData.lastdata).utc().valueOf(),
            pointInterval: 3600 * 1000, // 1h
            marker: {
              radius: 0,
            },
          },
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} km/h',
        },
        series: [
          {
            name: 'wind_speed_maxi_young',
            label: 'Vitesse du vent maxi',
          },
          {
            name: 'wind_direction_maxi_young',
            label: 'Direction du vent maxi',
            type: 'windbarb',
          },
        ],
      })
    },
    chartAirTempOptions() {
      return this.dataFor({
        title: {
          text: 'Température Air',
        },
        xAxis: {
          type: 'datetime',
        },
        plotOptions: {
          series: {
            pointStart: moment(this.flowCaptData.lastdata).utc().valueOf(),
            pointInterval: 3600 * 1000, // 1h
            marker: {
              radius: 0,
            },
          },
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} °C',
        },
        series: [
          {
            name: 'air_temperature_mean_nc',
            label: "Température de l'air",
          },
        ],
      })
    },
    chartAirHumidityOptions() {
      return this.dataFor({
        title: {
          text: 'Humidité air',
        },
        xAxis: {
          type: 'datetime',
        },
        plotOptions: {
          series: {
            pointStart: moment(this.flowCaptData.lastdata).utc().valueOf(),
            pointInterval: 3600 * 1000, // 1h
            marker: {
              radius: 0,
            },
          },
        },
        tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x:%e. %b %H:%M}: {point.y:.2f} %',
        },
        series: [
          {
            name: 'air_humidity_mean_nc',
            label: "Humidité de l'air",
          },
        ],
      })
    },
  },
  methods: {
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
              data: this.flowCaptData.measures[serieKey],
            }
          })
        graphMetaData.chart = { zoomType: 'x' }
        return graphMetaData
      } catch (e) {
        this.$store.commit(types.SET_ALERT, {
          level: alertTypes.DANGER,
          message: 'Error drawing charts',
        })
      }
    },
    dataForWind(graphMetaData) {
      try {
        const seriesKeys = Object.keys(
          this.flowCaptData.measures
        ).filter((serie) =>
          graphMetaData.series.map((e) => e.name).includes(serie)
        )

        const measures = this.flowCaptData.measures

        const windbarb = {
          type: 'windbarb',
          name: graphMetaData.series[0].label,
          data: measures[seriesKeys[0]].map((measure, index) => {
            return [measure, measures[seriesKeys[1]][index]]
          }),
        }

        const area = {
          type: 'area',
          name: graphMetaData.series[1].label,
          keys: ['y', 'rotation'],
          data: measures[seriesKeys[0]].map((measure, index) => {
            return [measure, measures[seriesKeys[1]][index]]
          }),
        }
        graphMetaData.series = [windbarb, area]
        graphMetaData.chart = { zoomType: 'x' }
        return graphMetaData
      } catch (e) {
        this.$store.commit(types.SET_ALERT, {
          level: alertTypes.DANGER,
          message: 'Error drawing charts',
        })
      }
    },
  },
}
</script>
