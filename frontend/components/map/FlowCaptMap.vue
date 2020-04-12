<template>
  <client-only>
    <div>
      <vl-layer-vector id="flowCaptStationLayer" render-mode="image">
        <!-- <vl-style-func :factory="myStyleFunc" /> -->
        <vl-source-vector
          :v-if="flowCaptStations"
          :features="flowCaptStations.features"
        ></vl-source-vector>
        <!-- <vl-style-box>
          <vl-style-circle :radius="5">
            <vl-style-stroke color="white"></vl-style-stroke>
            <vl-style-fill color="red"></vl-style-fill>

          </vl-style-circle>
        </vl-style-box> -->
      </vl-layer-vector>
      <!-- get all selection event. This up to us to handle everything and dispatch -->
      <vl-interaction-select :features.sync="selectedFeatures">
        <vl-overlay
          v-for="feature in selectedFeatures"
          :id="feature.id"
          :key="feature.id"
          :position="feature.geometry.coordinates"
          :auto-pan="true"
          :auto-pan-animation="{ duration: 300 }"
          class="feature-popup"
        >
          <b-card :title="'Site ' + feature.properties.fcs_site">
            <b-card-text>
              <ul>
                <li v-for="(v, k) in feature.properties" :key="v">
                  <em>{{ k }}</em> : {{ v }}
                </li>
              </ul>
            </b-card-text>
            <b-button :to="'/flowcapt/' + feature.properties.fcs_id">
              voir les données
            </b-button>
          </b-card>
        </vl-overlay>
      </vl-interaction-select>
    </div>
  </client-only>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      zoom: 5,
      center: [3.845, 45.506],
      rotation: 0,
      attribution: ['IGN-F/Géoportail'],
      url: process.env.baseMapUrl,
      baseLayerName: 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD',
      matrixSet: 'PM',
      format: 'image/jpeg',
      styleName: 'normal',
      selectedFeatures: [],
    }
  },
  computed: mapState(['flowCaptStations']),
}
</script>

<style>
#vl-map-map {
  width: 100%;
  height: 500px;
}
</style>
