<template>
  <div>
    <div v-for="alert in alerts" :key="alert.id">
      <alert-comp :alert="alert" />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Alert from '@/components/alert/Alert'

export default {
  components: {
    'alert-comp': Alert
  },
  computed: mapState(['alerts'])
}
</script>
