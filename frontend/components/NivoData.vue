<template>
  <div>
    <highcharts :options="chartOptions"></highcharts>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      chartOptions: {
        series: [
          {
            data: [1, 2, 3] // sample data
          }
        ]
      },
      records: []
    }
  },
  computed: mapState(['nivoseData'])
}
</script>
