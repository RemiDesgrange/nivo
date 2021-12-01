<template>
  <div>
    <div v-if="flowCaptData">
      <b-overlay :show="flowCaptLoading">
        <snow />
        <wind />
        <temperature />
      </b-overlay>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Snow from '~/components/chart/flowcapt/Snow'
import Wind from '~/components/chart/flowcapt/Wind'
import Temperature from '~/components/chart/flowcapt/Temperature'

export default {
  components: {
    Temperature,
    Wind,
    Snow
  },
  computed: mapState(['flowCaptData', 'flowCaptLoading'])
}
</script>
