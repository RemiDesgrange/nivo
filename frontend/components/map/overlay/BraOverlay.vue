<template>
  <b-card no-body class="overflow-hidden" bg-variant="light">
    <b-row no-gutters>
      <b-card-body>
        <b-card-title class="captialize-text">
          {{ name.toLowerCase() }}
        </b-card-title>
        <b-card-text>
          Dernier Bra:
          {{ formatDateStr(bradata.date) }}
        </b-card-text>
      </b-card-body>
    </b-row>
    <b-row no-gutters class="bra-indicator-overlay">
      <b-col>
        <input-orientation :value="bradata.dangerous_slopes" />
      </b-col>
      <b-col>
        <div class="bra-risk-indicator">
          <bra-indicator-svg
            :risk="bradata.max_risk"
            :risk-high="getRisk(bradata.risks, 'high')"
            :risk-low="getRisk(bradata.risks, 'low')"
            :altitude-thresold="getAltitudeThreshold(bradata.risks)"
          />
        </div>
      </b-col>
    </b-row>
    <b-row v-if="displayLink" no-gutters>
      <b-card-body>
        <b-button size="sm" :to="name.toLowerCase()">
          Voir le BRA
        </b-button>
      </b-card-body>
    </b-row>
  </b-card>
</template>

<script>
import moment from 'moment'
import InputOrientation from '~/components/utils/InputOrientation'
import BraIndicatorSvg from '~/components/utils/BraIndicatorSvg'

export default {
  components: {
    InputOrientation,
    BraIndicatorSvg
  },
  props: {
    name: {
      type: String,
      required: true
    },
    bradata: {
      type: Object,
      required: true
    },
    displayLink: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    getRisk (risks, level) {
      if (risks.length === 1) {
        return null
      }
      switch (level) {
        case 'high': {
          const riskHigh = risks.find(r => r.altitude.charAt(0) === '>')
          if (riskHigh) { return riskHigh.risk }
          break
        }
        case 'low': {
          const riskLow = risks.find(r => r.altitude.charAt(0) === '<')
          if (riskLow) { return riskLow.risk }
          break
        }
      }
    },
    getAltitudeThreshold (risks) {
      if (risks) {
        if (risks.length === 1) {
          return null
        }
        return parseInt(risks[0].altitude.substring(1))
      }
    },
    formatDateStr (dateStr) {
      return moment(new Date(dateStr)).format('DD/MM/YYYY')
    }
  }
}
</script>

<style scoped>
.captialize-text {
  text-transform: capitalize;
}

.card-title {
  font-size: 1rem;
  margin-bottom: 0rem;
}
.card-text {
  font-size: 0.75rem;
}
.bra-risk-indicator {
  position: relative;
  margin-left: -30px;
  margin-top: -20px;
}
</style>
