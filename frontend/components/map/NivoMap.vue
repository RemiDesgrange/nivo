<template>
  <div>
    <!-- nivo station -->
    <vl-layer-vector id="nivoStationLayer" render-mode="image">
      <vl-source-vector v-if="nivoStations" :features="nivoStations.features">
      </vl-source-vector>
      <vl-style-box>
        <vl-style-circle :radius="5">
          <vl-style-stroke color="white"></vl-style-stroke>
          <vl-style-fill color="red"></vl-style-fill>
        </vl-style-circle>
      </vl-style-box>
    </vl-layer-vector>

    <!-- get all selection event. This up to us to handle everything and dispatch -->
    <vl-interaction-select :features.sync="selectedFeatures">
      <vl-overlay
        v-for="feature in selectedFeatures"
        :key="feature.id"
        :id="feature.id"
        :position="feature.geometry.coordinates"
        :auto-pan="true"
        :auto-pan-animation="{ duration: 300 }"
        class="feature-popup"
      >
        <b-card :title="'Site ' + feature.properties.nss_name">
          <b-card-text>
            <ul>
              <li v-for="(v, k) in feature.properties">
                <em>{{ k }}</em> : {{ v }}
              </li>
            </ul>
          </b-card-text>
          <b-button :to="'/poste-nivo/' + feature.properties.nss_id">
            voir les données
          </b-button>
        </b-card>
      </vl-overlay>
    </vl-interaction-select>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data() {
    return {
      selectedFeatures: []
    }
  },
  computed: mapState(['nivoStations'])
}
</script>
