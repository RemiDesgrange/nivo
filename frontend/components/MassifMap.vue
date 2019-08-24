<template>
  <div>
    <no-ssr>
      <vl-map
        id="map"
        :load-tiles-while-animating="true"
        :load-tiles-while-interacting="true"
        data-projection="EPSG:4326"
      >
        <vl-view
          :zoom.sync="zoom"
          :center.sync="center"
          :rotation.sync="rotation"
        ></vl-view>
        <vl-layer-tile>
          <vl-source-osm></vl-source-osm>
        </vl-layer-tile>
      </vl-map>
    </no-ssr>
  </div>
</template>

<script>
export default {
  data() {
    return {
      zoom: 2,
      center: [0, 0],
      rotation: 0
    }
  }
}
</script>

<style>
#map {
  height: 400px;
}
</style>
