<template>
  <!-- inspired by https://github.com/c2corg/c2c_ui/blob/3b1c1628bf944a9cb94c53c68fd05d4d25c997ce/src/views/portals/YetiView.vue -->
  <div class="value-bra-container">
    <svg viewBox="0 0 100 100" width="120" height="120">
      <polygon
        style="fill: none; stroke: #000; stroke-miterlimit: 10;"
        points="2.2,89.5 97.5,89.5 62.7,11.9 48,32.9 31.8,25.5 "
      />
      <line
        v-if="isDifferent"
        style="fill: none; stroke: #000; stroke-miterlimit: 10;"
        x1="15"
        y1="61.5"
        x2="85"
        y2="61.5"
      />
    </svg>
    <div
      v-if="risk"
      class="value-bra-risk"
      :class="isDifferent ? 'value-bra-risk-different' : 'value-bra-risk-alone'"
    >
      <p aria-label="Niveau de danger BRA">
        {{ risk }}
      </p>
    </div>
    <div v-else>
      <img src="~/assets/R-1_70.png" class="img-no-risk" alt="Pas de risque" />
    </div>

    <div v-if="isDifferent" class="value-bra-high">
      <p aria-label="Niveau de danger BRA haut">
        {{ riskHigh }}
      </p>
    </div>

    <div v-if="isDifferent" class="value-bra-threshold">
      <p class="is-small">{{ altitudeThresold }}m</p>
    </div>

    <div v-if="isDifferent" class="value-bra-low">
      <p aria-label="Niveau de danger BRA bas">
        {{ riskLow }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    risk: {
      type: Number,
      validator: (val) => val > 0 && val < 6,
      default: null,
    },
    riskHigh: {
      type: Number,
      validator: (val) => val > 0 && val < 6,
      default: null,
    },
    riskLow: {
      type: Number,
      validator: (val) => val > 0 && val < 6,
      default: null,
    },
    altitudeThresold: {
      type: Number,
      default: null,
    },
  },
  computed: {
    isDifferent() {
      return !!(this.riskHigh && this.riskLow)
    },
  },
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
  left: 42px;
  top: 40px;
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
/*.value-bra-high {*/
/*  top: 45px;*/
/*}*/
</style>
