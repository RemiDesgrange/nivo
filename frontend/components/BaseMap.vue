<template>
  <client-only>
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
        <vl-source-wmts
          :attributions="attribution"
          :url="url"
          :layer-name="baseLayerName"
          :matrix-set="matrixSet"
          :format="format"
          :style-name="styleName"
        ></vl-source-wmts>
      </vl-layer-tile>

      <!-- Massif -->
      <vl-layer-vector id="massifLayer" render-mode="image">
        <vl-source-vector
          v-if="massifs"
          :features="massifs.features"
        ></vl-source-vector>
        <vl-style-box>
          <vl-style-stroke color="rgba(120,200,200,1)"></vl-style-stroke>
          <vl-style-fill color="rgba(200,255,255,0.8)"></vl-style-fill>
        </vl-style-box>
      </vl-layer-vector>
      <vl-overlay
        v-for="feature in selectedMassifFeature"
        :id="'popup-massif' + feature.id"
        :key="feature.id"
        :position="findPointOnSurface(feature)"
      >
        <b-card :title="feature.properties.name">
          <b-card-text>
            maybe some BRA infos ??
          </b-card-text>
        </b-card>
      </vl-overlay>

      <!-- nivo station -->
      <vl-layer-vector
        v-if="displayNivose"
        id="nivoStationLayer"
        render-mode="image"
      >
        <vl-source-vector
          v-if="nivoseStations"
          :features="nivoseStations.features"
        >
        </vl-source-vector>
        <!-- <vl-style-circle :radius="5">
          <vl-style-stroke color="rgba(255,255,0,0.4)"></vl-style-stroke>
          <vl-style-fill color="#ff0"></vl-style-fill>
        </vl-style-circle> -->
      </vl-layer-vector>

      <vl-overlay
        v-for="feature in selectedNivoFeature"
        :id="'popup-nivo' + feature.id"
        :key="feature.id"
        :position="findPointOnSurface(feature)"
      >
        <b-card :title="feature.properties.nss_name">
          <b-card-text>
            ..
          </b-card-text>
        </b-card>
      </vl-overlay>
      <!-- get all selection event. This up to us to handle everything and dispatch -->
      <vl-interaction-select
        :features.sync="selectedFeatures"
      ></vl-interaction-select>
    </vl-map>
  </client-only>
</template>

<script>
import 'vuelayers/lib/style.css'
import { pointOnFeature, booleanPointInPolygon } from '@turf/turf'
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
      selectedMassifFeature: [],
      selectedNivoFeature: [],
      displayNivose: true
    }
  },
  computed: mapState(['massifs', 'nivoseStations']),
  watch: {
    selectedFeatures(val) {
      this.selectedFeatures = val
      if (val[0]) {
        // FIXME this is ugly.
        this.$store.dispatch('fetchLastBraById', val[0].properties.id)
        this.findNivoStationInExtent(val[0].geometry).forEach((id) => {
          this.$store.dispatch('fetchLastNivoseById', id)
        })
      }
    }
  },
  methods: {
    findPointOnSurface(feature) {
      const point = pointOnFeature(feature.geometry)
      return point.geometry.coordinates
    },
    zoomToExtent(e) {
      console.log(e)
    },
    findNivoStationInExtent(geometry) {
      if (this.nivoseStations) {
        return this.nivoseStations.features
          .filter((f) => {
            booleanPointInPolygon(f, geometry)
          })
          .map((f) => f.properties.id)
      }
    }
  }
}
</script>

<style>
#map {
  width: 100%;
}
.captialize-text {
  text-transform: capitalize;
}
</style>
