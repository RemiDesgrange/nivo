<template>
  <div>
    <alert-comp :v-for="alert in alerts" :alert="alert" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Alert from '@/components/alert/Alert'

export default {
  components: {
    'alert-comp': Alert
  },
  computed: mapState('alerts')
}
</script>
