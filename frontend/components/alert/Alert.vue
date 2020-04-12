<template>
  <div>
    <b-alert
      :variant="alert.level"
      :show="duration"
      dismissible
      @dismissed="REMOVE_ALERT(alert)"
      @dismiss-count-down="countDownChanged"
    >
      <p>{{ alert.message }}</p>

      <p>This alert will dismiss after {{ alert.duration }} seconds...</p>
      <b-progress
        :variant="alert.level"
        :max="duration"
        :value="alert.duration"
        height="4px"
      ></b-progress>
    </b-alert>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  props: {
    alert: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      duration: this.alert.duration,
    }
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.DECREASE_ALERT_DURATION({
        alert: this.alert,
        newDuration: dismissCountDown,
      })
    },
    ...mapMutations(['DECREASE_ALERT_DURATION', 'REMOVE_ALERT']),
  },
}
</script>
