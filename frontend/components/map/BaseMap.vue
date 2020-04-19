<template>
  <div>
    <!--      <vl-map-->
    <!--        id="map"-->
    <!--        ref="map"-->
    <!--        :load-tiles-while-animating="true"-->
    <!--        :load-tiles-while-interacting="true"-->
    <!--        data-projection="EPSG:4326"-->
    <!--      >-->
    <!--        <vl-view-->
    <!--          :zoom.sync="zoom"-->
    <!--          :center.sync="center"-->
    <!--          :rotation.sync="rotation"-->
    <!--        ></vl-view>-->
    <!--        <vl-layer-group id="mapBaseLayersGroup">-->
    <!--          <vl-layer-tile-->
    <!--            v-for="layer in baseLayers"-->
    <!--            :key="layer.layerName"-->
    <!--            :visible="layer.visible"-->
    <!--          >-->
    <!--            <component :is="layer.cmp" v-bind="layer" />-->
    <!--          </vl-layer-tile>-->
    <!--        </vl-layer-group>-->

    <!--        <vl-layer-group id="mapSlopesLayerGroup">-->
    <!--          <vl-layer-tile :opacity="slopesOpacity" :visible="slopes.visible">-->
    <!--            <component :is="slopes.cmp" v-bind="slopes" />-->
    <!--          </vl-layer-tile>-->
    <!--        </vl-layer-group>-->

    <!--        <vl-layer-group id="mapFeaturesLayersGroup">-->
    <!--          <slot></slot>-->
    <!--        </vl-layer-group>-->
    <!--      </vl-map>-->
    <div id="map"></div>
    <slot></slot>
    <div class="ol-control ol-control-layer-switcher">
      <b-button v-b-toggle.collapse-layer-tree variant="light" size="sm">
        <!--                  <font-awesome-icon icon="layer-group" />-->
        <b-icon-layers />
      </b-button>
      <b-collapse id="collapse-layer-tree">
        <b-form-group label="Fond de plan">
          <b-form-radio-group v-model="selectBaseLayer" stacked>
            <b-form-radio
              v-for="layer in GET_BASE_LAYERS"
              :key="layer.get('name')"
              :value="layer.get('name')"
              name="baselayers-radio"
              >{{ layer.get('label') }}
            </b-form-radio>
          </b-form-radio-group>
        </b-form-group>
        <hr />
        <p>Pentes</p>
        <b-form-checkbox v-model="slopesVisibility" name="slopes" switch>
          IGN 30°/40°/45°
        </b-form-checkbox>
        <b-form-input
          v-model="slopesOpacity"
          type="range"
          min="0"
          max="1"
          step="0.1"
        ></b-form-input>
        <hr />
        <p>Couche</p>
        <b-form-checkbox switch>
          test
        </b-form-checkbox>
      </b-collapse>
    </div>
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

export default {
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
