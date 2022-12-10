<template>
  <div class="ol-control ol-control-layer-switcher">
    <b-button v-b-toggle.collapse-layer-tree variant="light" size="sm">
      <b-icon-layers />
    </b-button>
    <b-collapse id="collapse-layer-tree">
      <b-form-group label="Fond de plan">
        <b-form-radio-group v-model="selectBaseLayerName" stacked>
          <b-form-radio
            v-for="layer in baseLayers"
            :key="layer.get('name')"
            :value="layer.get('name')"
            name="baselayers-radio"
          >
            {{ layer.get('label') }}
          </b-form-radio>
        </b-form-radio-group>
      </b-form-group>
      <hr>
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
      />
      <b-form-checkbox v-model="skiTracksVisibility" name="skiTracks" switch>
        Piste de ski
      </b-form-checkbox>
      <hr>
      <p>Couche</p>
      <b-form-checkbox
        v-model="flowCaptVisibility"
        name="flowcaptStations"
        switch
      >
        Station FlowCapt
      </b-form-checkbox>
      <b-form-checkbox v-model="massifVisibility" name="massifs" switch>
        Massif
      </b-form-checkbox>
      <b-form-checkbox
        v-model="nivoStationVisibility"
        name="nivoStation"
        switch
      >
        Poste nivo
      </b-form-checkbox>
    </b-collapse>
  </div>
</template>

<script>
import { mapMutations, mapActions } from 'vuex'

import { mapMutationTypes, mapGettersTypes } from '~/modules/stateTypes'

export default {
  computed: {
    baseLayers () {
      return this.$mapService.baseLayers.getLayersArray()
    },
    selectedBaseLayer () {
      return this.$mapService.baseLayers.getLayersArray().find(l => l.getVisible())
    },
    ...mapActions('map', [
      mapGettersTypes.GET_BASE_LAYERS,
      mapGettersTypes.SELECTED_BASE_LAYER
    ]),
    slopesOpacity: {
      get () {
        return this.$mapService.slopes.getOpacity()
      },
      set (val) {
        this.SET_SLOPES_OPACITY(parseFloat(val))
      }
    },
    slopesVisibility: {
      get () {
        return this.$mapService.slopes.getVisible()
      },
      set (val) {
        this.SET_SLOPES_VISIBILITY(Boolean(val))
      }
    },
    skiTracksVisibility: {
      get () {
        return this.$mapService.skiTracks.getVisible()
      },
      set (val) {
        this.SET_SKI_TRACKS_VISIBILITY(Boolean(val))
      }
    },
    flowCaptVisibility: {
      get () {
        return this.$mapService.flowcapt.getVisible()
      },
      set (val) {
        this.SET_FLOWCAPT_VISIBILITY(Boolean(val))
      }
    },
    massifVisibility: {
      get () {
        return this.$mapService.massifs.getVisible()
      },
      set (val) {
        this.SET_MASSIFS_VISIBILITY(Boolean(val))
      }
    },
    nivoStationVisibility: {
      get () {
        return this.$mapService.posteNivo.getVisible()
      },
      set (val) {
        this.SET_NIVO_STATION_VISIBILITY(Boolean(val))
      }
    },
    selectBaseLayerName: {
      get () {
        return this.selectedBaseLayer.get('name')
      },
      set (val) {
        this.SET_SELECTED_BASE_LAYER(val)
      }
    }
  },
  methods: {
    ...mapMutations('map', [
      mapMutationTypes.SET_SLOPES_OPACITY,
      mapMutationTypes.SET_SELECTED_BASE_LAYER,
      mapMutationTypes.SET_SLOPES_VISIBILITY,
      mapMutationTypes.SET_SKI_TRACKS_VISIBILITY,
      mapMutationTypes.SET_NIVO_STATION_VISIBILITY,
      mapMutationTypes.SET_FLOWCAPT_VISIBILITY,
      mapMutationTypes.SET_MASSIFS_VISIBILITY
    ])
  }
}
</script>
