<template>
  <client-only>
    <div>
      <vl-layer-vector id="flowCaptStationLayer" render-mode="image">
        <vl-style-func :factory="myStyleFunc" />
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
import 'vuelayers/lib/style.css'
import { mapState } from 'vuex'
import Fill from 'ol/style/Fill'
import Stroke from 'ol/style/Stroke'
import Circle from 'ol/style/Circle'
import Style from 'ol/style/Style'

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
  computed: mapState(['flowCaptStations']),
  methods: {
    myStyleFunc() {
      return (feature) => {
        const fill = new Fill({
          color: feature.values_.fcs_altitude > 2000 ? 'black' : 'white'
        })
        const stroke = new Stroke({
          color: '#3399CC',
          width: 1.25
        })

        return new Style({
          image: new Circle({
            fill,
            stroke,
            radius: 5
          }),
          fill,
          stroke
        })
      }
    }
  }
}
</script>

<style>
#vl-map-map {
  width: 100%;
  height: 500px;
}
</style>
