import VectorSource from 'ol/source/Vector'
import VectorLayer from 'ol/layer/Vector'
import { massifsStyleFunc } from '~/modules/mapUtils'

export default new VectorLayer({
  source: new VectorSource({
    name: 'massifsSource'
  }),
  name: 'massifsLayer',
  style: massifsStyleFunc
})
