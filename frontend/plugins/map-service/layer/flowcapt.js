import VectorSource from 'ol/source/Vector'
import VectorLayer from 'ol/layer/Vector'
import { flowcaptStyleFunc } from '~/modules/mapUtils'

export default new VectorLayer({
  source: new VectorSource({
    name: 'flowcaptSource'
  }),
  name: 'flowcaptLayer',
  style: flowcaptStyleFunc
})
