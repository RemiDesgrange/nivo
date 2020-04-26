<template>
  <div>
    <div id="map"></div>
    <slot></slot>
    <ol-layer-tree />
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState, mapMutations } from 'vuex'

import {
  mapMutationTypes,
  mapGettersTypes,
  mapActionsTypes,
} from '~/modules/stateTypes'
import 'ol/ol.css'
import OlLayerTree from '~/components/map/OlLayerTree'

export default {
  components: {
    OlLayerTree,
  },
  computed: {
    ...mapGetters('map', [
      mapGettersTypes.GET_BASE_LAYERS,
      mapGettersTypes.SELECTED_BASE_LAYER,
    ]),
    ...mapState('map', ['map', 'slopes']),
    slopesOpacity: {
      get() {
        return this.slopes.getOpacity()
      },
      set(val) {
        this.SET_SLOPES_OPACITY(val)
      },
    },
    slopesVisibility: {
      get() {
        return this.slopes.getVisible()
      },
      set(val) {
        this.SET_SLOPES_VISIBILITY(val)
      },
    },
    selectBaseLayer: {
      get() {
        return this.SELECTED_BASE_LAYER
      },
      set(val) {
        this.SET_SELECTED_BASE_LAYER(val)
      },
    },
  },
  mounted() {
    this.INIT_MAP()
  },
  methods: {
    ...mapActions('map', [mapActionsTypes.INIT_MAP]),
    ...mapMutations('map', [
      mapMutationTypes.SET_SLOPES_OPACITY,
      mapMutationTypes.SET_SELECTED_BASE_LAYER,
      mapMutationTypes.SET_SLOPES_VISIBILITY,
    ]),
  },
}
</script>

<style>
#map-container {
  width: 100%;
  height: 100%;
}

#map {
  width: 100%;
  height: 50vh;
}

.ol-control-layer-switcher {
  bottom: 0.5em;
  left: 1.5em;
}

.ol-control button {
  color: black;
  background-color: white;
}

.ol-control button:hover,
.ol-control button:focus {
  color: black;
  background-color: darkgray;
}

/*.map-panel {*/
/*  position: absolute;*/
/*  display: inline-block;*/
/*  top: 2em;*/
/*  right: 2em;*/
/*  text-align: left;*/
/*}*/

/*.captialize-text {*/
/*  text-transform: capitalize;*/
/*}*/
</style>
