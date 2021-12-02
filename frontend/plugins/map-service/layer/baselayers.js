import LayerGroup from 'ol/layer/Group'
import WMTS from 'ol/source/WMTS'
import XYZ from 'ol/source/XYZ'
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

export default new LayerGroup({
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
        tileGrid: getIgnTileGrid()
      }),
      visible: true,
      name: 'ign',
      label: 'Carte IGN'
    }),
    new TileLayer({
      source: new XYZ({
        url:
          'https://api.mapbox.com/styles/v1/brankgnol/ck05b5qfv08zp1cqxpcpmmuc5/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYnJhbmtnbm9sIiwiYSI6IjNVUmliWG8ifQ.QfnRYCCoSPUqX0Z4tr_Rjg',
        label: 'Carte enrichie données station',
        attributions: 'Brankgnol/Mapbox',
        layer: 'Outdoors winter web'
      }),
      name: 'brankgnol',
      label: 'Outdoors winter web',
      visible: false
    }),
    new TileLayer({
      source: new XYZ({
        url: 'https://b.tile.opentopomap.org/{z}/{x}/{y}.png',
        attributions:
          '© OpenStreetMap-Mitwirkende, SRTM | Kartendarstellung: © OpenTopoMap (CC-BY-SA)'
      }),
      visible: false,
      name: 'opentopomap',
      label: 'OpenTopoMap'
    })
  ]
})
