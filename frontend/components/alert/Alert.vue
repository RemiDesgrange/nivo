<template>
  <div>
    <!-- <b-alert
      dismissible
      :variant="alert.level"
      @dismissed="alert.level = 0"
      @dismiss-count-down="countDownChanged"
    >
      <p>{{ alert.message }}</p>

      <p>This alert will dismiss after {{ dismissCountDown }} seconds...</p>
      <b-progress
        :variant="alert.level"
        :max="duration"
        :value="alert.duration"
        height="4px"
      ></b-progress>
    </b-alert> -->
    <p>{{ alert }}</p>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  props: {
    alert: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      duration: 10 // this.alert.duration
    }
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.DECREASE_ALERT_DURATION(this.alert.message, dismissCountDown)
    },
    ...mapMutations(['DECREASE_ALERT_DURATION'])
  }
}
</script>
