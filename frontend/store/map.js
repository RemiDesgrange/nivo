import VectorLayer from 'ol/layer/Vector'
import { pointerMove, click } from 'ol/events/condition'
import GeoJSON from 'ol/format/GeoJSON'
import {
  mapMutationTypes as types,
  mapGettersTypes as getterTypes
} from '@/modules/stateTypes'
import { mapActionsTypes } from '~/modules/stateTypes'

export const state = () => ({
  // features selected by ol/interraction/Select. Since ol6, we can have multiple Select in 1 page
  selectedFeatures: {
    flowcapt: {
      byHover: [],
      byClick: [],
      byApp: []
    },
    posteNivo: {
      byHover: [],
      byClick: [],
      byApp: []
    },
    massifs: {
      byHover: [],
      byClick: [],
      byApp: []
    }
  }
})

export const getters = {
  [getterTypes.SELECTED_MASSIF_CLICK] (state) {
    return state.selectedFeatures.massifs.byClick
  },
  [getterTypes.SELECTED_MASSIF_HOVER] (state) {
    return state.selectedFeatures.massifs.byHover
  },
  [getterTypes.SELECTED_MASSIF] (state) {
    return state.selectedFeatures.massifs.byApp
  },
  [getterTypes.SELECTED_FLOWCAPT_STATION_CLICK] (state) {
    return state.selectedFeatures.flowcapt.byClick
  },
  [getterTypes.SELECTED_FLOWCAPT_STATION_HOVER] (state) {
    return state.selectedFeatures.flowcapt.byHover
  },
  [getterTypes.SELECTED_NIVO_STATION_HOVER] (state) {
    return state.selectedFeatures.posteNivo.byHover
  },
  [getterTypes.SELECTED_NIVO_STATION_CLICK] (state) {
    return state.selectedFeatures.posteNivo.byClick
  }
}

export const actions = {
  [mapActionsTypes.INIT_MAP] ({ commit, state }) {
    commit(types.ADD_LAYER, this.$mapService.baseLayers)
    commit(types.ADD_LAYER, this.$mapService.slopes)
    commit(types.ADD_LAYER, this.$mapService.massifs)
    commit(types.ADD_LAYER, this.$mapService.flowcapt)
    commit(types.ADD_LAYER, this.$mapService.posteNivo)
    const layersWithInteratcions = ['flowcapt', 'posteNivo', 'massifs']
    layersWithInteratcions.forEach((e) => {
      commit(
        types.ADD_INTERACTION,
        {
          layer: e,
          options: {
            collection: 'byClick',
            condition: click
          }
        }
      )
      commit(
        types.ADD_INTERACTION,
        {
          layer: e,
          options: {
            collection: 'byHover',
            condition: pointerMove
          }
        })
      // we want to be able to select features programmaticaly

      commit(
        types.ADD_INTERACTION,
        {
          layer: e,
          options: {
            collection: 'byApp',
            condition: null
          }
        }
      )
    })
    commit(types.SET_TARGET, document.getElementById('map'))
  },
  [mapActionsTypes.ADD_FEATURES] ({ commit }, { layer, features }) {
    commit('ADD_FEATURES', { layer, features })
  },
  [getterTypes.GET_BASE_LAYERS] () {
    return this.$mapService.getBaseLayers().getLayers().getArray()
  },
  [getterTypes.SELECTED_BASE_LAYER] () {
    const selected = this.$mapService.getBaseLayers()
      .getLayers()
      .getArray()
      .find(l => l.getVisible())
    return selected.get('name')
  }
}

export const mutations = {
  [types.ADD_TO_SELECTED_FEATURES] (state, { layer, collection, feature }) {
    state.selectedFeatures[layer][collection].length = 0
    state.selectedFeatures[layer][collection].push(feature)
  },
  [types.REMOVE_FROM_SELECTED_FEATURES] (state, { layer, collection, feature }) {
    state.selectedFeatures[layer][collection].pop()
  },
  [types.SET_TARGET] (state, target) {
    this.$mapService.map.setTarget(target)
  },
  [types.SET_VIEW] (state, view) {
    this.$mapService.map.setView(view)
  },
  [types.ADD_LAYER] (state, layer) {
    const isAlreadyExist = this.$mapService.map
      .getLayers()
      .getArray()
      .find(l => l.get('name') === layer.get('name'))
    if (!isAlreadyExist) {
      this.$mapService.map.addLayer(layer)
    }
  },
  [types.SET_LAYER] (state, layer) {
    layer.setMap(this.$mapService.map)
  },
  [types.REMOVE_LAYER] (state, layer) {
    this.$mapService.map.removeLayer(layer)
  },
  [types.ADD_OVERLAY] (state, overlay) {
    this.$mapService.map.addOverlay(overlay)
  },
  [types.REMOVE_OVERLAY] (state, overlay) {
    this.$mapService.map.removeOverlay(overlay)
  },
  [types.ADD_INTERACTION] (state, { layer, options }) {
    this.$mapService.addInteraction(layer, options)
  },
  [types.REMOVE_INTERACTION] (state, interaction) {
    this.$mapService.map.removeInteraction(interaction)
  },
  [types.FIT_VIEW] (state, extent) {
    this.$mapService.map.getView().fit(extent)
  },
  [types.CLEAN_SELECTED_FEATURES] (_, selectedCollection) {
    selectedCollection.length = 0
  },
  [types.ADD_FEATURES] (state, { layerName, features }) {
    const layer = this.$mapService.map
      .getLayers()
      .getArray()
      .find(l => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().addFeatures(features)
    }
  },
  [types.ADD_FEATURE] (state, { layerName, feature }) {
    const layer = this.$mapService.map
      .getLayers()
      .getArray()
      .find(l => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().addFeature(feature)
    }
  },
  [types.SET_FEATURES] (state, { layerName, features }) {
    const layer = this.$mapService.map
      .getLayers()
      .getArray()
      .find(l => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().clear()
      layer.getSource().addFeatures(features)
    }
  },
  [types.SET_FEATURE] (state, { layerName, feature }) {
    const layer = this.$mapService.map
      .getLayers()
      .getArray()
      .find(l => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().clear()
      layer.getSource().addFeature(feature)
    }
  },
  [types.SET_RAW_GEOJSON] (state, { layerName, geojson }) {
    try {
      this.$mapService[layerName].getSource().clear()
      this.$mapService[layerName].getSource().addFeatures(
        new GeoJSON().readFeatures(geojson, {
          dataProjection: 'EPSG:4326',
          featureProjection: 'EPSG:3857'
        })
      )
    } catch (e) {
      console.error(`cannot set geojson in ${layerName}`)
    }
  },
  [types.SET_SELECTED_BASE_LAYER] (state, layerName) {
    // only 1 base layer can be visible
    this.$mapService.getBaseLayers()
      .getLayers()
      .getArray()
      .filter(l => l.get('name') === layerName)
      .map(l => l.setVisible(true))
  },
  [types.SET_MASSIFS_VISIBILITY] (state, value) {
    this.$mapService.massifs.setVisible(value)
    this.$mapService.map.render()
  },
  [types.SET_FLOWCAPT_VISIBILITY] (state, value) {
    this.$mapService.flowcapt.setVisible(value)
    this.$mapService.map.render()
  },
  [types.SET_NIVO_STATION_VISIBILITY] (state, value) {
    this.$mapService.posteNivo.setVisible(value)
    this.$mapService.map.render()
  },
  [types.SET_SLOPES_VISIBILITY] (state, value) {
    this.$mapService.slopes.setVisible(value)
    this.$mapService.map.render() // it seems that render needs to be trigger in case of visible no idea why.
  },
  [types.SET_SLOPES_OPACITY] (state, value) {
    this.$mapService.slopes.setOpacity(value)
  },
  [types.SET_VISIBILITY] (state, { layerName, visibility }) {
    try {
      this.$mapService[layerName].setVisible(visibility)
    } catch (ex) {
      console.error('cannot set visibility of layer ' + layerName)
    }
  },
  [types.SET_SELECTED_MASSIF] (state, massif) {
    if (massif) {
      const f = this.$mapService.massifs
        .getSource()
        .getFeatures()
        .find(f => f.get('id') === massif.id)
      this.$mapService.setSelectedFeatures('massifs', f)
    }
  },
  [types.SET_SELECTED_FLOWCAPT_STATION] (state, flowcapt) {
    if (flowcapt) {
      const f = this.$mapService.flowcapt
        .getSource()
        .getFeatures()
        .find(f => f.get('fcs_id') === flowcapt.properties.fcs_id)
      this.$mapService.setSelectedFeatures('flowcapt', f)
    }
  },
  [types.SET_SELECTED_NIVO_STATION] (state, station) {
    if (station) {
      const f = this.$mapService.posteNivo
        .getSource()
        .getFeatures()
        .find(f => f.get('nss_id') === station.properties.nss_id)
      this.$mapService.setSelectedFeatures('posteNivo', f)
    }
  }
}
