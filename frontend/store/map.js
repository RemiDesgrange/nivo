import { Map as OlMap } from 'ol'
import View from 'ol/View'
import LayerGroup from 'ol/layer/Group'
import WMTS from 'ol/source/WMTS'
import XYZ from 'ol/source/XYZ'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import Collection from 'ol/Collection'
import Select from 'ol/interaction/Select'
import GeoJSON from 'ol/format/GeoJSON'
import { pointerMove, click } from 'ol/events/condition'
import WMTSTileGrid from 'ol/tilegrid/WMTS'
import { get as getProjection } from 'ol/proj'
import { getWidth } from 'ol/extent'
import {
  massifsStyleFunc,
  // selectionStyleBasedOnExisting,
} from '~/modules/mapUtils'
import {
  mapMutationTypes as types,
  mapGettersTypes as getterTypes,
} from '@/modules/stateTypes'
import { mapActionsTypes } from '~/modules/stateTypes'

function _getIgnTileGrid() {
  const resolutions = []
  const matrixIds = []
  const proj3857 = getProjection('EPSG:3857')
  const maxResolution = getWidth(proj3857.getExtent()) / 256

  for (let i = 0; i < 18; i++) {
    matrixIds[i] = i.toString()
    resolutions[i] = maxResolution / 2 ** i
  }

  return new WMTSTileGrid({
    origin: [-20037508, 20037508],
    resolutions,
    matrixIds,
  })
}

export const state = () => ({
  map: new OlMap(),
  view: new View({
    projection: 'EPSG:3857',
    // center: [2.438, 46.528],
    center: [465455.0376565846, 6020157.832574354],
    zoom: 5.8,
  }),
  baseLayers: new LayerGroup({
    name: 'baselayers',
    layers: [
      new TileLayer({
        source: new WMTS({
          url: process.env.ignBaseMapURL,
          layer: 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD',
          matrixSet: 'PM',
          format: 'image/jpeg',
          attributions: 'IGN-F/Géoportail',
          style: 'normal',
          projection: 'EPSG:3857',
          tileGrid: _getIgnTileGrid(),
        }),
        visible: true,
        name: 'ign',
        label: 'Carte IGN',
      }),
      new TileLayer({
        source: new XYZ({
          url:
            'https://api.mapbox.com/styles/v1/brankgnol/ck05b5qfv08zp1cqxpcpmmuc5/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYnJhbmtnbm9sIiwiYSI6IjNVUmliWG8ifQ.QfnRYCCoSPUqX0Z4tr_Rjg',
          label: 'Carte enrichie données station',
          attributions: 'Brankgnol/Mapbox',
          layer: 'Outdoors winter web',
        }),
        name: 'brankgnol',
        label: 'Outdoors winter web',
        visible: false,
      }),
      new TileLayer({
        source: new XYZ({
          url: 'https://b.tile.opentopomap.org/{z}/{x}/{y}.png',
          attributions:
            '© OpenStreetMap-Mitwirkende, SRTM | Kartendarstellung: © OpenTopoMap (CC-BY-SA)',
        }),
        visible: false,
        name: 'opentopomap',
        label: 'OpenTopoMap',
      }),
    ],
  }),
  slopes: new TileLayer({
    source: new WMTS({
      url: process.env.ignBaseMapURL,
      layer: 'GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN',
      matrixSet: 'PM',
      format: 'image/png',
      attributions: 'IGN-F/Géoportail',
      style: 'normal',
      projection: 'EPSG:3857',
      tileGrid: _getIgnTileGrid(),
    }),
    name: 'slopes',
    opacity: 0.5,
    visible: true,
  }),
  flowcapt: new VectorLayer({
    source: new VectorSource({
      name: 'flowcaptSource',
    }),
    name: 'flowcaptLayer',
  }),
  posteNivo: new VectorLayer({
    source: new VectorSource({
      name: 'posteNivoSource',
    }),
    name: 'posteNivoLayer',
  }),
  massifs: new VectorLayer({
    source: new VectorSource({
      name: 'massifsSource',
    }),
    name: 'massifsLayer',
    style: massifsStyleFunc,
  }),
  // features selected by ol/interraction/Select. Since ol6, we can have multiple Select in 1 page
  selectedFeatures: {
    flowcapt: {
      byHover: new Collection(),
      byClick: new Collection(),
      byApp: new Collection(),
    },
    posteNivo: {
      byHover: new Collection(),
      byClick: new Collection(),
      byApp: new Collection(),
    },
    massifs: {
      byHover: new Collection(),
      byClick: new Collection(),
      byApp: new Collection(),
    },
  },
})

export const getters = {
  [getterTypes.GET_BASE_LAYERS](state) {
    return state.baseLayers.getLayers().getArray()
  },
  [getterTypes.SELECTED_BASE_LAYER](state) {
    const selected = state.baseLayers
      .getLayers()
      .getArray()
      .find((l) => l.getVisible())
    return selected.get('name')
  },
  [getterTypes.SELECTED_MASSIF_CLICK](state) {
    return state.selectedFeatures.massifs.byClick.getArray()
  },
  [getterTypes.SELECTED_MASSIF_HOVER](state) {
    return state.selectedFeatures.massifs.byHover.getArray()
  },
  [getterTypes.SELECTED_FLOWCAPT_STATION_CLICK](state) {
    return state.selectedFeatures.flowcapt.byClick.getArray()
  },
  [getterTypes.SELECTED_FLOWCAPT_STATION_HOVER](state) {
    return state.selectedFeatures.flowcapt.byHover.getArray()
  },
  [getterTypes.SELECTED_NIVO_STATION_HOVER](state) {
    return state.selectedFeatures.posteNivo.byHover.getArray()
  },
  [getterTypes.SELECTED_NIVO_STATION_CLICK](state) {
    return state.selectedFeatures.posteNivo.byClick.getArray()
  },
}

export const actions = {
  [mapActionsTypes.INIT_MAP]({ commit, state }) {
    commit(types.ADD_LAYER, state.baseLayers)
    commit(types.SET_LAYER, state.slopes)
    commit(types.SET_LAYER, state.massifs)
    commit(types.SET_LAYER, state.flowcapt)
    commit(types.SET_LAYER, state.posteNivo)
    // interactions
    const layersWithInteratcions = ['flowcapt', 'posteNivo', 'massifs']
    layersWithInteratcions.forEach((e) => {
      commit(
        types.ADD_INTERACTION,
        new Select({
          features: state.selectedFeatures[e].byClick,
          layers: [state[e]],
          condition: click,
        })
      )
      commit(
        types.ADD_INTERACTION,
        new Select({
          features: state.selectedFeatures[e].byHover,
          layers: [state[e]],
          condition: pointerMove,
        })
      )
      // we want to be able to select features programmaticaly
      commit(
        types.ADD_INTERACTION,
        new Select({
          features: state.selectedFeatures[e].byApp,
          layers: [state[e]],
          condition: null,
        })
      )
    })
    commit(types.SET_TARGET, document.getElementById('map'))
    commit(types.SET_VIEW, state.view)
  },
  [mapActionsTypes.ADD_FEATURES]({ commit }, { layer, features }) {
    commit('ADD_FEATURES', { layer, features })
  },
}

export const mutations = {
  [types.SET_TARGET](state, target) {
    state.map.setTarget(target)
  },
  [types.SET_VIEW](state, view) {
    state.map.setView(view)
  },
  [types.ADD_LAYER](state, layer) {
    const isAlreadyExist = state.map
      .getLayers()
      .getArray()
      .find((l) => l.get('name') === layer.get('name'))
    if (!isAlreadyExist) {
      state.map.addLayer(layer)
    }
  },
  [types.SET_LAYER](state, layer) {
    layer.setMap(state.map)
  },
  [types.REMOVE_LAYER](state, layer) {
    state.map.removeLayer(layer)
  },
  [types.ADD_OVERLAY](state, overlay) {
    state.map.addOverlay(overlay)
  },
  [types.REMOVE_OVERLAY](state, overlay) {
    state.map.removeOverlay(overlay)
  },
  [types.ADD_INTERACTION](state, interaction) {
    state.map.addInteraction(interaction)
  },
  [types.REMOVE_INTERACTION](state, interaction) {
    state.map.removeInteraction(interaction)
  },
  [types.FIT_VIEW](state, extent) {
    state.view.fit(extent)
  },
  [types.CLEAN_SELECTED_FEATURES](_, selectedCollection) {
    selectedCollection.clear()
  },
  [types.ADD_FEATURES](state, { layerName, features }) {
    const layer = state.map
      .getLayers()
      .getArray()
      .find((l) => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().addFeatures(features)
    }
  },
  [types.ADD_FEATURE](state, { layerName, feature }) {
    const layer = state.map
      .getLayers()
      .getArray()
      .find((l) => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().addFeature(feature)
    }
  },
  [types.SET_FEATURES](state, { layerName, features }) {
    const layer = state.map
      .getLayers()
      .getArray()
      .find((l) => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().clear()
      layer.getSource().addFeatures(features)
    }
  },
  [types.SET_FEATURE](state, { layerName, feature }) {
    const layer = state.map
      .getLayers()
      .getArray()
      .find((l) => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().clear()
      layer.getSource().addFeature(feature)
    }
  },
  [types.SET_RAW_GEOJSON](state, { layerName, geojson }) {
    try {
      state[layerName].getSource().clear()
      state[layerName].getSource().addFeatures(
        new GeoJSON().readFeatures(geojson, {
          dataProjection: 'EPSG:4326',
          featureProjection: 'EPSG:3857',
        })
      )
    } catch (e) {
      console.warn(`cannot set geojson in ${layerName}`)
    }
  },
  [types.SET_SELECTED_BASE_LAYER](state, layerName) {
    // only 1 base layer can be visible
    state.baseLayers
      .getLayers()
      .getArray()
      .forEach((l) => {
        if (l.get('name') === layerName) {
          l.setVisible(true)
        } else {
          l.setVisible(false)
        }
      })
  },
  // TODO need to be actions that go fetch the data if they don't exist !!
  [types.SET_MASSIFS_VISIBILITY](state, value) {
    state.massifs.setVisible(value)
    state.map.render()
  },
  [types.SET_FLOWCAPT_VISIBILITY](state, value) {
    state.flowcapt.setVisible(value)
    state.map.render()
  },
  [types.SET_NIVO_STATION_VISIBILITY](state, value) {
    state.posteNivo.setVisible(value)
    state.map.render()
  },
  [types.SET_SLOPES_VISIBILITY](state, value) {
    state.slopes.setVisible(value)
    state.map.render() // it seems that render needs to be trigger in case of visible no idea why.
  },
  [types.SET_SLOPES_OPACITY](state, value) {
    state.slopes.setOpacity(value)
  },
  [types.SET_VISIBILITY](state, { layerName, visibility }) {
    try {
      state[layerName].setVisible(visibility)
    } catch (ex) {
      console.warn('cannot set visibility of layer ' + layerName)
    }
  },
  [types.SET_SELECTED_MASSIF](state, massif) {
    if (massif) {
      const f = state.massifs
        .getSource()
        .getFeatures()
        .find((f) => f.get('id') === massif.id)
      state.selectedFeatures.massifs.byApp.clear()
      state.selectedFeatures.massifs.byApp.push(f)
    }
  },
  [types.SET_SELECTED_FLOWCAPT_STATION](state, flowcapt) {
    if (flowcapt) {
      const f = state.flowcapt
        .getSource()
        .getFeatures()
        .find((f) => f.get('fcs_id') === flowcapt.properties.fcs_id)
      state.selectedFeatures.flowcapt.byApp.clear()
      state.selectedFeatures.flowcapt.byApp.push(f)
    }
  },
  [types.SET_SELECTED_NIVO_STATION](state, station) {
    if (station) {
      const f = state.posteNivo
        .getSource()
        .getFeatures()
        .find((f) => f.get('nss_id') === station.properties.nss_id)
      state.selectedFeatures.posteNivo.byApp.clear()
      state.selectedFeatures.posteNivo.byApp.push(f)
    }
  },
}
