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
    <vl-layer-vector render-mode="image" ref="massifLayer">
      <vl-source-vector :url="massifs" v-if="massifs">
      </vl-source-vector>
      <vl-style-box>
        <vl-style-stroke color="rgba(120,200,200,1)"></vl-style-stroke>
        <vl-style-fill color="rgba(200,255,255,0.8)"></vl-style-fill>
      </vl-style-box>
    </vl-layer-vector>
    <vl-interaction-select :features.sync="selectedMassifFeature" :layers="massifLayer"/>
    <vl-overlay
      v-for="feature in selectedMassifFeature"
      :key="feature.properties.id"
      :id="'popup-' + feature.properties.id"
      :position="findPointOnSurface(feature)"
    >
      <div>
        propr massif {{ feature.properties.name }}
      </div>
    </vl-overlay>

    <!-- nivo station -->
    <vl-layer-vector render-mode="image" ref="nivoLayer">
      <vl-source-vector :url="nivoStation" v-if="nivoStation">
      </vl-source-vector>
    </vl-layer-vector>
    <vl-interaction-select :features.sync="selectedNivoFeature" :layer="nivoLayer"/>
    <vl-overlay
      v-for="feature in selectedNivoFeature"
      :key="feature.properties.id"
      :id="'popup-' + feature.properties.id"
      :position="findPointOnSurface(feature)"
    >
      <div>
        propr nivo {{ feature.properties.nss_name }}
      </div>
    </vl-overlay>
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
  SelectInteraction
} from 'vuelayers'
import ZoomSlider from 'ol/control/ZoomSlider'
import 'vuelayers/lib/style.css'
import pointOnFeature from '@turf/point-on-feature'

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
      selectedMassifFeature: [],
      selectedNivoFeature: [],
      massifLayer: [],
      nivoLayer: []
    }
  },
  methods: {
    onMapMounted() {
      this.$refs.map.$map.getControls().extend([new ZoomSlider()])
    },
    findPointOnSurface(feature) {
      const point = pointOnFeature(feature)
      return point.geometry.coordinates
    }
  },
  mounted() {
    this.massifLayer.push(this.$refs.massifLayer)
    this.nivoLayer.push(this.$refs.nivoLayer)
  }
}
</script>

<style>
#map {
  width: 100%;
}
</style>
