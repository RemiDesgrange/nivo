<template>
  <div>
    <base-area-chart
      title="Température de l'air"
      :series="airTemperature"
      :point-start="lastData"
      y-axis-text="Témpérature (°C)"
      y-axis-label="{value} °C"
    />
    <base-area-chart
      title="Humidité de l'air"
      :series="airHumidity"
      :point-start="lastData"
      y-axis-text="Humidité (%)"
      y-axis-label="{value} %"
    />
  </div>
</template>

<script>
// import BaseAreaChart from "~/components/chart/BaseAreaChart"
import FlowCaptChartMixin from '~/components/chart/flowcapt/FlowCaptChartMixin'

export default {
  mixins: [FlowCaptChartMixin],
  computed: {
    airHumidity () {
      return [
        {
          data: this.flowCaptData.measures.air_humidity_mean_nc,
          type: 'area',
          name: "Température de l'air"
        }
      ]
    },
    airTemperature () {
      return [
        {
          data: this.flowCaptData.measures.air_temperature_mean_nc,
          type: 'area',
          name: "Humidité de l'air"
        }
      ]
    }
  }
}
</script>
