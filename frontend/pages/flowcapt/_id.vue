<template>
  <div id="app">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <h1>Station {{ flowCaptData.station }}</h1>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <flow-capt-chart />
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <base-map>
              <flow-capt-map />
            </base-map>
          </div>
          <div class="w-100"></div>
          <div class="col">
            <h2>
              <a :href="flowCaptData.url" target="_blank">liens ISAW</a>
            </h2>
            <dl v-if="selectedFlowCaptStation">
              <dt>Station</dt>
              <dd>{{ selectedFlowCaptStation.properties.fcs_id }}</dd>
              <dt>label</dt>
              <dd>{{ selectedFlowCaptStation.properties.fcs_site }}</dd>
              <dt>pays</dt>
              <dd>{{ selectedFlowCaptStation.properties.fcs_country }}</dd>
              <dt>Dernier relevé</dt>
              <dd v-if="oldLastData(flowCaptData.lastdata)">
                {{ flowCaptData.lastdata }}
                <b-icon
                  id="lastDataIndicatorKo"
                  :style="{ color: 'red' }"
                  icon="x"
                  font-scale="2"
                />
              </dd>
              <dd v-else>
                {{ flowCaptData.lastdata }}
                <b-icon
                  id="lastDataIndicatorOk"
                  :style="{ color: 'green' }"
                  icon="check"
                  font-scale="1.5"
                />
              </dd>
            </dl>
            <b-tooltip target="lastDataIndicatorOk" placement="right">
              Le capteur à envoyé ses données à {{ flowCaptData.lastdata }}
            </b-tooltip>
            <b-tooltip target="lastDataIndicatorKo" placement="right">
              Le capteur à envoyé ses données il y a plus d'une journée
              {{ flowCaptData.lastdata }}
            </b-tooltip>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'
import FlowCaptChart from '@/components/chart/FlowCaptChart'

import FlowCaptMap from '@/components/map/FlowCaptMap'
import BaseMap from '@/components/map/BaseMap'
import {
  // globalMutationTypes as mutationsType,
  globalActionsTypes as actionsType,
  mapMutationTypes,
} from '~/modules/stateTypes'

export default {
  components: {
    FlowCaptMap,
    FlowCaptChart,
    BaseMap,
  },
  async asyncData({ store, params }) {
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'massifs',
      visibility: false,
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'flowcapt',
      visibility: true,
    })
    store.commit('map/' + mapMutationTypes.SET_VISIBILITY, {
      layerName: 'posteNivo',
      visibility: false,
    })
    await store.dispatch(actionsType.FETCH_FLOWCAPT_STATIONS)
    await store.dispatch(actionsType.FETCH_FLOWCAPT_DATA, params.id)
    store.dispatch(
      actionsType.SET_SELECTED_FLOWCAPT_STATION,
      store.state.flowCaptStations.features.find(
        (e) => e.properties.fcs_id === params.id
      )
    )
  },
  computed: {
    ...mapState([
      'flowCaptData',
      'flowCaptStations',
      'selectedFlowCaptStation',
    ]),
  },
  methods: {
    oldLastData(dateAsStr) {
      return moment().diff(moment(dateAsStr), 'days') > 1
    },
  },
}
</script>
