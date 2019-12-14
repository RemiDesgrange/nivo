<template>
  <div>
    <!-- nivo station -->
    <vl-layer-vector id="nivoStationLayer" render-mode="image">
      <vl-source-vector
        v-if="nivoStations"
        ref="nivoStationsSourceVector"
        :features="nivoStations.features"
      >
      </vl-source-vector>
      <vl-style-box>
        <vl-style-circle :radius="5">
          <vl-style-stroke color="white"></vl-style-stroke>
          <vl-style-fill color="red"></vl-style-fill>
        </vl-style-circle>
      </vl-style-box>
    </vl-layer-vector>

    <!-- get all selection event. This up to us to handle everything and dispatch -->
    <!-- slice of coordinates is to eliminate the Z index -->
    <vl-interaction-select :features.sync="selectedFeatures">
      <vl-overlay
        v-for="feature in selectedFeatures"
        :id="feature.id"
        :key="feature.id"
        :position="feature.geometry.coordinates.slice(0, 2)"
        :auto-pan="true"
        :auto-pan-animation="{ duration: 300 }"
        class="feature-popup"
      >
        <b-card :title="'Site ' + feature.properties.nss_name">
          <b-card-text>
            <ul>
              <li><em>Altitude</em> {{ feature.geometry.coordinates[2] }}</li>
              <li>
                <em>Identifiant Météo France</em>
                {{ feature.properties.nss_meteofrance_id }}
              </li>
            </ul>
          </b-card-text>
          <b-button :to="'/poste-nivo/' + feature.properties.nss_id">
            voir les données
          </b-button>
        </b-card>
      </vl-overlay>
    </vl-interaction-select>
    <div>selected features : {{ selectedFeatures }}</div>
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
  computed: mapState(['nivoStations', 'selectedNivoStation']),
  watch: {
    selectedNivoStation(value) {
      if (value === null) {
        this.selectedFeatures = []
      } else {
        this.selectedFeatures = this.$refs.nivoStationsSourceVector
          .getFeatures()
          .filter((f) => f.getProperties().nss_id === value.properties.nss_id)
          .map((f) => {
            value.id = f.getId()
            return value
          })
      }
    }
  }
}
</script>
