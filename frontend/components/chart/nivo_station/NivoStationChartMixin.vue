<script>
import { Chart } from 'highcharts-vue'
import { mapState } from 'vuex'
import moment from 'moment'
import BaseAreaChart from '~/components/chart/BaseAreaChart'

export default {
  components: {
    Chart,
    BaseAreaChart
  },
  computed: {
    ...mapState(['nivoData']),
    lastData () {
      if (this.nivoData.length > 0) {
        const lastDate = moment(this.nivoData.slice().reverse().pop().date)
        return lastDate.utc().valueOf()
      }
      return null
    }
  }
}
</script>
