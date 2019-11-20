<template>
  <client-only>
    <div>
      <vl-map
        id="map"
        ref="map"
        :load-tiles-while-animating="true"
        :load-tiles-while-interacting="true"
        data-projection="EPSG:4326"
      >
        <vl-view
          :zoom.sync="zoom"
          :center.sync="center"
          :rotation.sync="rotation"
        ></vl-view>
        <vl-layer-tile id="baseLayer">
          <!-- <vl-source-wmts
            :attributions="attribution"
            :url="url"
            :layer-name="baseLayerName"
            :matrix-set="matrixSet"
            :format="format"
            :style-name="styleName"
          ></vl-source-wmts> -->
          <vl-source-osm></vl-source-osm>
        </vl-layer-tile>

        <vl-layer-vector id="flowCaptStationLayer" render-mode="image">
          <vl-source-vector
            v-if="flowCaptStations"
            :features="flowCaptStations.features"
          ></vl-source-vector>
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
            <b-card :title="'Site ' + feature.properties.fcs_site">
              <b-card-text>
                <ul>
                  <li v-for="(v, k) in feature.properties">
                    <em>{{ k }}</em> : {{ v }}
                  </li>
                </ul>
              </b-card-text>
              <b-button :to="'/flowcapt/' + feature.properties.fcs_id"
                >voir les données</b-button
              >
            </b-card>
          </vl-overlay>
        </vl-interaction-select>
      </vl-map>
      <div>{{ selectedFeatures }}</div>
    </div>
  </client-only>
</template>

<script>
import 'vuelayers/lib/style.css'
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
      selectedFeatures: []
    }
  },
  computed: mapState(['flowCaptStations'])
}
</script>

<style>
#vl-map-map {
  width: 100%;
  height: 500px;
}
</style>
