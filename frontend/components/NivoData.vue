<template>
  <div>
    <div v-if="nivoDataLoading">
      <div class="text-center">
        <b-spinner type="grow" label="Spinning"></b-spinner>
      </div>
    </div>
    <div v-if="nivoData">
      <highcharts :options="chartOptions"></highcharts>
    </div>
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
  computed: mapState(['nivoData', 'nivoDataLoading'])
}
</script>
