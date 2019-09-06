<template>
  <div>
    <!-- nivo station -->
    <vl-layer-vector id="nivoStationLayer" render-mode="image">
      <vl-source-vector
        v-if="nivoStations"
        :features="nivoStations.features"
      ></vl-source-vector>
      <!-- <vl-style-circle :radius="5">
          <vl-style-stroke color="rgba(255,255,0,0.4)"></vl-style-stroke>
          <vl-style-fill color="#ff0"></vl-style-fill>
      </vl-style-circle>-->
    </vl-layer-vector>

    <vl-overlay
      v-for="feature in selectedNivoFeature"
      :id="'popup-nivo' + feature.id"
      :key="feature.id"
      :position="findPointOnSurface(feature)"
    >
      <b-card :title="feature.properties.nss_name">
        <b-card-text>..</b-card-text>
      </b-card>
    </vl-overlay>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data() {
    return {
      selectedNivoFeature: []
    }
  },
  computed: mapState(['nivoStations'])
}
</script>
