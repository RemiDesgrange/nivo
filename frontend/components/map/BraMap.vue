<template>
  <div>
    <!-- Massif -->
    <!--    <vl-layer-vector id="massifLayer" name="Massif" render-mode="image">-->
    <!--      <vl-source-vector-->
    <!--        v-if="massifs"-->
    <!--        :features="massifs.features"-->
    <!--      ></vl-source-vector>-->
    <!--      <vl-style-box>-->
    <!--        <vl-style-stroke color="rgba(120,200,200,1)"></vl-style-stroke>-->
    <!--        <vl-style-fill color="rgba(200,255,255,0.8)"></vl-style-fill>-->
    <!--      </vl-style-box>-->
    <!--    </vl-layer-vector>-->
    <!--    <vl-overlay-->
    <!--      v-for="feature in selectedMassifFeature"-->
    <!--      :id="'popup-massif' + feature.id"-->
    <!--      :key="feature.id"-->
    <!--      :position="findPointOnSurface(feature)"-->
    <!--    >-->
    <!--      <b-card :title="feature.properties.name">-->
    <!--        <b-card-text>maybe some BRA infos ??</b-card-text>-->
    <!--      </b-card>-->
    <!--    </vl-overlay>-->
    <ol-overlay
      v-for="feature in SELECTED_MASSIF_HOVER"
      :id="'popup-massif-hover' + feature.get('id')"
      :key="feature.id"
      class="massifHover"
      :position="feature"
    >
      <b-card
        :title="feature.get('name').toLowerCase()"
        class="captialize-text"
        bg-variant="light"
      >
        <b-card-text>
          <p>Risque {{ feature.get('latest_risk') }}</p>
          <p>Date: {{ formatDateStr(feature.get('latest_date')) }}</p>
        </b-card-text>
        <input-orientation :value="feature.get('latest_dangerous_slopes')" />
        <b-button :to="feature.get('name').toLowerCase()">Voir le BRA</b-button>
      </b-card>
    </ol-overlay>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import moment from 'moment'
import InputOrientation from '../utils/InputOrientation'
import OlOverlay from './OlOverlay'
import { mapGettersTypes } from '~/modules/stateTypes'

export default {
  components: {
    OlOverlay,
    InputOrientation,
  },
  computed: {
    ...mapState('map', ['massifs']),
    ...mapGetters('map', [
      mapGettersTypes.SELECTED_MASSIF_CLICK,
      mapGettersTypes.SELECTED_MASSIF_HOVER,
    ]),
  },
  methods: {
    formatDateStr(dateStr) {
      return moment(new Date(dateStr)).format('DD/MM/YYYY')
    },
  },
}
</script>

<style>
.captialize-text {
  text-transform: capitalize;
}
</style>
