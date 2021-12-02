import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'

import { nivoStationStyleFunc } from '~/modules/mapUtils'

export default new VectorLayer({
  source: new VectorSource({
    name: 'posteNivoSource'
  }),
  name: 'posteNivoLayer',
  style: nivoStationStyleFunc
})
