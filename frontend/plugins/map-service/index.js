import { Map as OlMap, View } from 'ol'
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
  constructor () {
    this.baseLayers = BaseLayers
    this.slopes = Slopes
    this.flowcapt = FlowCapt
    this.posteNivo = PosteNivo
    this.massifs = Massifs
  }

  getBaseLayer (sourceName) {
    return this.baseLayers[sourceName]
  }

  getBaseLayers () {
    return this.baseLayers
  }
}

export default MapService
