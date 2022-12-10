import XYZ from 'ol/source/XYZ'
import TileLayer from 'ol/layer/Tile'

export default new TileLayer({
  source: new XYZ({
    url: 'https://tiles.opensnowmap.org/pistes/{z}/{x}/{y}.png',
    attributions:
        '© www.opensnowmap.org (CC-BY-SA)'
  }),
  visible: false,
  name: 'opensnowmap',
  label: 'OpenSnowMap'
})
