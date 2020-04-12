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
  map: null, // a new map is created everytime you reload the basemap component.
  view: new View({
    projection: 'EPSG:4326',
    center: [2.438, 46.528],
    zoom: 5,
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
          attribution: ['IGN-F/Géoportail'],
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
          attribution: 'Brankgnol/Mapbox',
          layer: 'Outdoors winter web',
        }),
        name: 'brankgnol',
        label: 'Outdoors winter web',
        visible: false,
      }),
      new TileLayer({
        source: new XYZ({
          url: 'https://b.tile.opentopomap.org/{z}/{x}/{y}.png',
          attribution:
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
      attribution: ['IGN-F/Géoportail'],
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
      url: `${process.env.baseUrl}/bra/massifs`,
      format: new GeoJSON(),
    }),
    name: 'massifsLayer',
    style: massifsStyleFunc,
  }),
  // features selected by ol/interraction/Select. Since ol6, we can have multiple Select in 1 page
  selectedFeatures: {
    flowcapt: {
      byHover: new Collection(),
      byClick: new Collection(),
    },
    posteNivo: {
      byHover: new Collection(),
      byClick: new Collection(),
    },
    massifs: {
      byHover: new Collection(),
      byClick: new Collection(),
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
}

export const actions = {
  [mapActionsTypes.INIT_MAP]({ commit, state }) {
    commit(types.CREATE_MAP)
    commit(types.SET_TARGET, 'map')
    commit(types.SET_VIEW, state.view)
    commit(types.ADD_LAYER, state.baseLayers)
    commit(types.ADD_LAYER, state.slopes)
    commit(types.ADD_LAYER, state.massifs)
    commit(types.ADD_LAYER, state.flowcapt)
    commit(types.ADD_LAYER, state.posteNivo)
    // interactions
    const layersWithInteratcions = ['flowcapt', 'posteNivo', 'massifs']
    layersWithInteratcions.forEach((e) => {
      commit(
        types.ADD_INTERACTION,
        new Select({
          features: state.selectedFeatures.flowcapt.byClick,
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
    })
  },
  [mapActionsTypes.ADD_FEATURES]({ commit }, { layer, features }) {
    commit('ADD_FEATURES', { layer, features })
  },
}

export const mutations = {
  [types.CREATE_MAP](state) {
    state.map = new OlMap()
  },
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
  [types.REMOVE_LAYER](state, layer) {
    state.map.removeLayer(layer)
  },
  [types.ADD_OVERLAY](state, overlay) {
    state.map.addOverlay(overlay)
  },
  [types.REMOVE_OVERLAY](state, overlay) {
    state.map.removeOverlay(overlay)
  },
  [types.SET_OVERLAY_POSITION](state, { overlay, coordinate: coord }) {
    state[overlay].setPosition(coord)
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
    const layer = state.map
      .getLayers()
      .getArray()
      .find((l) => l.get('name') === layerName)
    if (layer instanceof VectorLayer) {
      layer.getSource().clear()
      layer.getSource().addFeatures(new GeoJSON().readFeatures(geojson))
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
  [types.SET_SLOPES_VISIBILITY](state, value) {
    state.slopes.setVisible(value)
  },
  [types.SET_SLOPES_OPACITY](state, value) {
    state.slopes.setOpacity(value)
  },
}
