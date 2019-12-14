<template>
  <client-only>
    <div id="map-container">
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
        <vl-layer-group id="mapBaseLayersGroup">
          <vl-layer-tile
            v-for="layer in baseLayers"
            :key="layer.layerName"
            :visible="layer.visible"
          >
            <component :is="layer.cmp" v-bind="layer" />
          </vl-layer-tile>
        </vl-layer-group>

        <vl-layer-group id="mapSlopesLayerGroup">
          <vl-layer-tile :opacity="slopesOpacity" :visible="slopes.visible">
            <component :is="slopes.cmp" v-bind="slopes" />
          </vl-layer-tile>
        </vl-layer-group>

        <vl-layer-group id="mapFeaturesLayersGroup">
          <slot></slot>
        </vl-layer-group>
      </vl-map>

      <div class="ol-control ol-control-layer-switcher">
        <b-button v-b-toggle.collapse-layer-tree variant="light" size="sm">
          <font-awesome-icon icon="layer-group" />
        </b-button>
        <b-collapse id="collapse-layer-tree">
          <b-form-group label="Fond de plan">
            <b-form-radio
              v-for="layer in baseLayers"
              :key="layer.layerName"
              v-model="selectedBaseLayer"
              :value="layer.layerName"
              name="baselayers-radio"
              >{{ layer.label }}</b-form-radio
            >
          </b-form-group>
          <hr />
          <p>Pentes</p>
          <b-form-checkbox v-model="slopes.visible" name="slopes" switch>
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
  </client-only>
</template>

<script>
export default {
  data() {
    return {
      zoom: 5,
      center: [3.845, 45.506],
      rotation: 0,
      baseLayers: [
        {
          cmp: 'vl-source-wmts',
          url: process.env.ignBaseMapURL,
          layerName: 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD',
          matrixSet: 'PM',
          format: 'image/jpeg',
          attribution: ['IGN-F/Géoportail'],
          styleName: 'normal',
          label: 'Carte IGN',
          visible: true
        },
        {
          cmp: 'vl-source-xyz',
          url:
            'https://api.mapbox.com/styles/v1/brankgnol/ck05b5qfv08zp1cqxpcpmmuc5/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYnJhbmtnbm9sIiwiYSI6IjNVUmliWG8ifQ.QfnRYCCoSPUqX0Z4tr_Rjg',
          layerName: 'Outdoors winter web',
          label: 'Carte enrichie données station',
          attribution: 'Brankgnol/Mapbox',
          visible: false
        },
        {
          cmp: 'vl-source-xyz',
          url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
          label: 'OpenTopoMap',
          layerName: 'opentopomap',
          attribution:
            '© OpenStreetMap-Mitwirkende, SRTM | Kartendarstellung: © OpenTopoMap (CC-BY-SA)',
          visible: false
        }
      ],
      slopes: {
        cmp: 'vl-source-wmts',
        url: process.env.ignBaseMapURL,
        layerName: 'GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN',
        matrixSet: 'PM',
        format: 'image/png',
        attribution: ['IGN-F/Géoportail'],
        styleName: 'normal',
        opacity: 0.5,
        visible: true
      }
    }
  },
  computed: {
    selectedBaseLayer: {
      get() {
        return this.baseLayers.find((l) => l.visible === true).layerName
      },
      set(newVal) {
        this.baseLayers.forEach((l) => {
          if (l.layerName === newVal) {
            l.visible = true
          } else {
            l.visible = false
          }
        })
      }
    },
    slopesOpacity: {
      get() {
        return this.slopes.opacity
      },
      set(newVal) {
        this.slopes.opacity = Number(newVal)
      }
    }
  }
}
</script>

<style>
#map-container {
  width: 100%;
  height: 100%;
}
#map {
  width: 100%;
  height: 100%;
}

.ol-control-layer-switcher {
  bottom: 0.5em;
  left: 1.5em;
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
