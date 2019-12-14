<template>
  <div>
    <!-- Massif -->
    <vl-layer-vector id="massifLayer" name="Massif" render-mode="image">
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
        <b-card-text>maybe some BRA infos ??</b-card-text>
      </b-card>
    </vl-overlay>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      selectedMassifFeature: []
    }
  },
  computed: mapState(['massifs'])
}
</script>
