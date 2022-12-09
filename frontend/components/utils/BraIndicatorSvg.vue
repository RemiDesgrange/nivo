<template>
  <!-- inspired by https://github.com/c2corg/c2c_ui/blob/3b1c1628bf944a9cb94c53c68fd05d4d25c997ce/src/views/portals/YetiView.vue -->
  <div class="value-bra-container">
    <svg viewBox="0 0 100 100" width="auto" height="100%">
      <polygon
        style="fill: none; stroke: #000; stroke-miterlimit: 10"
        points="2.2,89.5 97.5,89.5 62.7,11.9 48,32.9 31.8,25.5 "
      />
      <text v-if="(!isDifferent && risk)" style="fill: #000; font-family: Arial, sans-serif; font-size: 220%" x="40" y="70">{{ risk }}</text>
      <image
        v-if="!risk"
        href="~/assets/R-1_70.png"
        x="10"
        y="50"
        height="50"
        width="50"
      />
      <line
        v-if="isDifferent"
        style="fill: none; stroke: #000; stroke-miterlimit: 10"
        x1="15"
        y1="61.5"
        x2="85"
        y2="61.5"
      />
      <text v-if="isDifferent" style="fill: #000; font-family: Arial, sans-serif; font-size: 220%" x="0" y="45">{{ risk }}</text>
      <text v-if="isDifferent" style="fill: #000; font-family: Arial, sans-serif; font-size: 130%" x="45" y="55">{{ riskHigh }}</text>
      <text v-if="isDifferent" style="fill: #000; font-family: Arial, sans-serif; font-size: 130%" x="45" y="80">{{ riskLow }}</text>
      <text v-if="isDifferent" style="fill: #000; font-family: Arial, sans-serif; font-size: 50%" x="56" y="60">{{ altitudeThresold }}m</text>
    </svg>
  </div>
</template>

<script>
export default {
  props: {
    risk: {
      type: Number,
      validator: val => val > 0 && val < 6,
      default: null
    },
    riskHigh: {
      type: Number,
      validator: val => val > 0 && val < 6,
      default: null
    },
    riskLow: {
      type: Number,
      validator: val => val > 0 && val < 6,
      default: null
    },
    altitudeThresold: {
      type: Number,
      default: null
    }
  },
  computed: {
    isDifferent () {
      return !!(this.riskHigh && this.riskLow)
    }
  }
}
</script>

<style>
.value-bra-container {
  margin-left: 2rem;
  position: relative;
}

.value-bra-risk > p {
  font-size: 300%;
}
.value-bra-risk-alone {
  position: absolute;
  left: 35px;
  top: 30px;
}
.value-bra-risk-different {
  position: absolute;
  left: 0px;
  top: 0px;
}
.value-bra-high {
  position: absolute;
  left: 52px;
  top: 45px;
}
.value-bra-threshold {
  position: absolute;
  left: 115px;
  top: 60px;
  width: 85px;
}
.value-bra-low {
  position: absolute;
  left: 52px;
  top: 78px;
}
.img-no-risk {
  position: absolute;
  left: 30px;
  top: 55px;
  width: auto;
  height: 40%;
}
</style>
