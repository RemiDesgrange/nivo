<template>
  <vl-map
    id="map"
    ref="map"
    :load-tiles-while-animating="true"
    :load-tiles-while-interacting="true"
    data-projection="EPSG:4326"
    @mounted="onMapMounted"
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

    <vl-layer-tile id="slopes" :max-resolution="50" :opacity="0.75">
      <vl-source-wmts
        :attributions="attribution"
        :url="url"
        :layer-name="slopesLayerName"
        :matrix-set="matrixSet"
        format="image/png"
        :style-name="styleName"
      ></vl-source-wmts>
    </vl-layer-tile>
    <!-- Massif -->
    <vl-layer-vector render-mode="image" id="massifLayer">
      <vl-source-vector :url="massifs" v-if="massifs"> </vl-source-vector>
      <vl-style-box>
        <vl-style-stroke color="rgba(120,200,200,1)"></vl-style-stroke>
        <vl-style-fill color="rgba(200,255,255,0.8)"></vl-style-fill>
      </vl-style-box>
    </vl-layer-vector>
    <vl-overlay
      v-for="feature in selectedMassifFeature"
      :key="feature.id"
      :id="'popup-massif' + feature.id"
      :position="findPointOnSurface(feature)"
    >
      <b-card :title="feature.properties.name">
        <b-card-text>
          maybe some BRA infos ??
        </b-card-text>
      </b-card>
    </vl-overlay>

    <!-- nivo station -->
    <vl-layer-vector render-mode="image" id="nivoStationLayer">
      <vl-source-vector :url="nivoStation" v-if="nivoStation">
      </vl-source-vector>
    </vl-layer-vector>

    <vl-overlay
      v-for="feature in selectedNivoFeature"
      :key="feature.id"
      :id="'popup-nivo' + feature.id"
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
</template>

<script>
import Vue from 'vue'
import {
  Map,
  TileLayer,
  WmtsSource,
  VectorLayer,
  VectorSource,
  StyleBox,
  FillStyle,
  StrokeStyle,
  Overlay,
  SelectInteraction,
  StyleFunc
} from 'vuelayers'
import ZoomSlider from 'ol/control/ZoomSlider'
import 'vuelayers/lib/style.css'
import { pointOnFeature } from '@turf/turf'

Vue.use(Map)
Vue.use(TileLayer)
Vue.use(WmtsSource)
Vue.use(VectorLayer)
Vue.use(VectorSource)
Vue.use(StyleBox)
Vue.use(FillStyle)
Vue.use(StrokeStyle)
Vue.use(Overlay)
Vue.use(SelectInteraction)
Vue.use(StyleFunc)

export default {
  data() {
    return {
      zoom: 5,
      center: [3.845, 45.506],
      rotation: 0,
      attribution: ['IGN-F/Géoportail'],
      url: 'https://wxs.ign.fr/an7nvfzojv5wa96dsga5nk8w/geoportail/wmts',
      baseLayerName: 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD',
      matrixSet: 'PM',
      format: 'image/jpeg',
      styleName: 'normal',
      slopesLayerName: 'GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN',
      massifs: `http://localhost:9000/bra/massifs`,
      nivoStation: 'http://localhost:9000/nivo/stations',
      selectedFeatures: [],
      selectedMassifFeature: [],
      selectedNivoFeature: []
    }
  },
  methods: {
    onMapMounted() {
      this.$refs.map.$map.getControls().extend([new ZoomSlider()])
    },
    findPointOnSurface(feature) {
      const point = pointOnFeature(feature.geometry)
      return point.geometry.coordinates
    }
  },
  watch: {
    selectedFeatures(val) {
      this.selectedNivoFeature = val.filter(
        geojson => geojson.properties.nss_id || ''
      )
      this.selectedMassifFeature = val.filter(
        geojson => geojson.properties.department || ''
      )
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
