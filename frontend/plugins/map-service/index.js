import { Map as OlMap, View } from 'ol'
import Select from 'ol/interaction/Select'
import Collection from 'ol/Collection'
import { BaseLayers, Slopes, FlowCapt, PosteNivo, Massifs } from './layer'

class MapService {
  map = new OlMap({
    view: new View({
      projection: 'EPSG:3857',
      center: [453408.9918842213, 5461004.166551998],
      zoom: 5.8
    })
  })

  baseLayers = null
  slopes = null
  flowcapt = null
  posteNivo = null
  massifs = null

  #selectedFeatures = {
    flowcapt: {
      byHover: new Collection(),
      byClick: new Collection(),
      byApp: new Collection()
    },
    posteNivo: {
      byHover: new Collection(),
      byClick: new Collection(),
      byApp: new Collection()
    },
    massifs: {
      byHover: new Collection(),
      byClick: new Collection(),
      byApp: new Collection()
    }
  }

  #store = null

  constructor (store) {
    this.baseLayers = BaseLayers
    this.slopes = Slopes
    this.flowcapt = FlowCapt
    this.posteNivo = PosteNivo
    this.massifs = Massifs
    this.#store = store
  }

  getBaseLayer (sourceName) {
    return this.baseLayers[sourceName]
  }

  getBaseLayers () {
    return this.baseLayers
  }

  addInteraction (layer, options) {
    this.map.addInteraction(new Select({
      features: this.#selectedFeatures[layer][options.collection],
      layers: [this[layer]],
      condition: options.condition ?? null
    }))
    // populate back the store when collection is hydrated or suppressed.
    this.#selectedFeatures[layer][options.collection].on('add', (e) => {
      this.#store.commit('map/ADD_TO_SELECTED_FEATURES',
        { layer, collection: options.collection, feature: e.element })
    })
    this.#selectedFeatures[layer][options.collection].on('remove', (e) => {
      this.#store.commit('map/REMOVE_FROM_SELECTED_FEATURES',
        { layer, collection: options.collection, feature: e.element })
    })
  }

  setSelectedFeatures (layer, feature) {
    this.#selectedFeatures[layer].byApp.clear()
    this.#selectedFeatures[layer].byApp.push(feature)
  }
}

export default MapService
