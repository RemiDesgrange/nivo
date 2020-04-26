<script>
import { Chart } from 'highcharts-vue'
import { mapState } from 'vuex'
import moment from 'moment'
import BaseAreaChart from '~/components/chart/BaseAreaChart'

export default {
  components: {
    Chart,
    BaseAreaChart,
  },
  computed: {
    ...mapState(['flowCaptData']),
    lastData() {
      return moment(this.flowCaptData.lastdata).utc().valueOf()
    },
  },
}
</script>
