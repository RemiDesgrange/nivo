<template>
 <vl-map :load-tiles-while-animating="true" :load-tiles-while-interacting="true" data-projection="EPSG:4326" style="height: 400px">
    <vl-view :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>
    <vl-layer-tile id="baseLayer">
      <vl-source-wmts
        :attributions="attribution"
        :url="url"
        :layer-name="baseLayerName"
        :matrix-set="matrixSet"
        :format="format"
        :style-name="styleName">
        </vl-source-wmts>
    </vl-layer-tile>

    <vl-layer-tile id="slopes">
      <vl-source-wmts
        :attributions="attribution"
        :url="url"
        :layer-name="slopesLayerName"
        :matrix-set="matrixSet"
        format="image/png"
        :style-name="styleName">
        </vl-source-wmts>
    </vl-layer-tile>

    <vl-layer-vector v-if="massifs.length">
      <vl-source-vector :features="massifs">
      </vl-source-vector>
    </vl-layer-vector>
  </vl-map>
</template>

<script>
import Vue from 'vue'
import { Map, TileLayer, WmtsSource, VectorLayer, VectorSource } from 'vuelayers'
import 'vuelayers/lib/style.css'
import axios from 'axios'

Vue.use(Map)
Vue.use(TileLayer)
Vue.use(WmtsSource)
Vue.use(VectorLayer)
Vue.use(VectorSource)

export default {
  data () {
    return {
        zoom: 5,
        center: [3.845, 45.506],
        rotation: 0,
        attribution: ["IGN-F/Géoportail"],
        url: 'https://wxs.ign.fr/an7nvfzojv5wa96dsga5nk8w/geoportail/wmts',
        baseLayerName: 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD',
        matrixSet: 'PM',
        format: 'image/jpeg',
        styleName: 'normal',
        slopesLayerName: 'GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN',
        massifs: []
    }
  },
  mounted () {
    axios.get('http://localhost:8000/bra/massifs')
    .then(response => {
      this.massifs = response.data.features
    })
    .catch(e => {
      alert(e)
    })
  }
}
</script>
