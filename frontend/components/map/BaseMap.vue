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

      <bra-map />

      <nivo-map />

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
import { mapActions, mapMutations } from 'vuex'
import NivoMap from '@/components/map/NivoMap'
import BraMap from '@/components/map/BraMap'

export default {
  components: {
    NivoMap,
    BraMap
  },
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
      displayNivo: true
    }
  },
  watch: {
    selectedFeatures(val) {
      this.selectedFeatures = val
      if (val[0]) {
        // FIXME this is ugly.
        this.fetchLastBraById(val[0].properties.id)
        this.findNivoStationInExtent(val[0].geometry).forEach((id) => {
          this.fetchLastNivoById(id)
        })
      }
    }
  },
  methods: {
    findPointOnSurface(feature) {
      const point = pointOnFeature(feature.geometry)
      return point.geometry.coordinates
    },
    findNivoStationInExtent(geometry) {
      if (this.nivoStations) {
        return this.nivoStations.features
          .filter((f) => {
            booleanPointInPolygon(f, geometry)
          })
          .map((f) => f.properties.id)
      }
    },
    ...mapActions(['fetchLastNivoById', 'fetchLastBraById']),
    ...mapMutations(['selectBra'])
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
