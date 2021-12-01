<template>
  <div>
    <base-area-chart
      y-axis-text="centimètre"
      y-axis-label="{value} cm"
      :series="snowQuantity"
      title="Hauteur de neige"
      :point-start="lastData"
    />
    <base-area-chart
      y-axis-text="g/m²/s"
      y-axis-label="{value}"
      :series="snowDrift"
      title="Quantité de neige transporté par le vent"
      :point-start="lastData"
    />
  </div>
</template>
<script>
import FlowCaptChartMixin from '~/components/chart/flowcapt/FlowCaptChartMixin'

export default {
  mixins: [FlowCaptChartMixin],
  computed: {
    snowQuantity () {
      return [
        {
          type: 'area',
          name: 'Hauteur Seg1',
          data: this.flowCaptData.measures.snow_height_seg1_nc
        },
        {
          type: 'area',
          name: 'Hauteur Seg2',
          data: this.flowCaptData.measures.snow_height_seg2_nc
        }
      ]
    },
    snowDrift () {
      return [
        {
          type: 'area',
          name: 'Déplacement de neige sonde 1',
          data: this.flowCaptData.measures.snow_drift_seg1_flowcapt
        },
        {
          type: 'area',
          name: 'Déplacement de neige sonde 2',
          data: this.flowCaptData.measures.snow_drift_seg2_flowcapt
        }
      ]
    }
  }
}
</script>
