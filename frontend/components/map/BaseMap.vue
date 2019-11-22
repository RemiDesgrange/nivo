<template>
  <client-only>
    <div id="map-container">
      <vl-map
        id="map"
        ref="map"
        :load-tiles-while-animating="true"
        :load-tiles-while-interacting="true"
        @mounted="onMapMounted"
        data-projection="EPSG:4326"
      >
        <vl-view
          :zoom.sync="zoom"
          :center.sync="center"
          :rotation.sync="rotation"
        ></vl-view>
        <vl-layer-group id="mapBaseLayersGroup">
          <vl-layer-tile id="baseLayer">
            <vl-source-xyz
              :attributions="attribution"
              :url="url"
              :layer-name="baseLayerName"
              :matrix-set="matrixSet"
              :format="format"
              :style-name="styleName"
            ></vl-source-xyz>
          </vl-layer-tile>
        </vl-layer-group>

        <vl-layer-group id="mapFeaturesLayersGroup">
          <slot></slot>
        </vl-layer-group>

        <!-- get all selection event. This up to us to handle everything and dispatch -->
        <!-- <vl-interaction-select
          :features.sync="selectedFeatures"
        ></vl-interaction-select> -->
      </vl-map>

      <div class="map-panel">
        <div>
          <b-form-checkbox name="pompom" switch>this is a test</b-form-checkbox>
        </div>
      </div>
    </div>
  </client-only>
</template>

<script>
import 'vuelayers/lib/style.css'

export default {
  data() {
    return {
      zoom: 5,
      center: [3.845, 45.506],
      rotation: 0,
      attribution: ['IGN-F/Géoportail'],
      url:
        'https://api.mapbox.com/styles/v1/brankgnol/ck05b5qfv08zp1cqxpcpmmuc5/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYnJhbmtnbm9sIiwiYSI6IjNVUmliWG8ifQ.QfnRYCCoSPUqX0Z4tr_Rjg',
      // 'https://api.mapbox.com/styles/v1/brankgnol/ck05b5qfv08zp1cqxpcpmmuc5/wmts?access_token=', // process.env.baseMapUrl,
      baseLayerName: 'Outdoors winter web', // 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD',
      matrixSet: 'EPSG:3857',
      format: 'image/jpeg',
      styleName: '',
      panelOpen: false,
      layers: false
    }
  },
  methods: {
    onMapMounted() {
      // The idea is to build the base layer group and the feature layer group
    }
  }
}
</script>

<style>
#map {
  width: 100%;
  height: 500px;
}
.ol-control button {
  color: black;
  background-color: white;
}
.map-panel {
  position: absolute;
  display: inline-block;
  top: 2em;
  right: 2em;
  text-align: left;
}
.captialize-text {
  text-transform: capitalize;
}
</style>
