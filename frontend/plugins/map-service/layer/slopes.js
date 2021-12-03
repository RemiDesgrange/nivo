import WMTS from 'ol/source/WMTS'
import TileLayer from 'ol/layer/Tile'
import WMTSTileGrid from 'ol/tilegrid/WMTS'
import { get as getProjection } from 'ol/proj'
import { getWidth } from 'ol/extent'

function getIgnTileGrid () {
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
    matrixIds
  })
}

export default new TileLayer({
  source: new WMTS({
    url: process.env.ignBaseMapURL,
    layer: 'GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN',
    matrixSet: 'PM',
    format: 'image/png',
    attributions: 'IGN-F/Géoportail',
    style: 'normal',
    projection: 'EPSG:3857',
    tileGrid: getIgnTileGrid()
  }),
  name: 'slopes',
  opacity: 0.5,
  visible: false
})
