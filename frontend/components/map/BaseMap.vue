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

      <slot></slot>

      <!-- get all selection event. This up to us to handle everything and dispatch -->
      <!-- <vl-interaction-select
        :features.sync="selectedFeatures"
      ></vl-interaction-select> -->
    </vl-map>
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
      url: process.env.baseMapUrl,
      baseLayerName: 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD',
      matrixSet: 'PM',
      format: 'image/jpeg',
      styleName: 'normal'
    }
  }
}
</script>

<style>
#vl-map-map {
  width: 100%;
  height: 500px;
}
.captialize-text {
  text-transform: capitalize;
}
</style>
