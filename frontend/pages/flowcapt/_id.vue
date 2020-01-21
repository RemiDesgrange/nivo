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
            <dl v-if="selectedStation">
              <dt>Station</dt>
              <dd>{{ selectedStation.properties.fcs_id }}</dd>
              <dt>label</dt>
              <dd>{{ selectedStation.properties.fcs_site }}</dd>
              <dt>pays</dt>
              <dd>{{ selectedStation.properties.fcs_country }}</dd>
              <dt>Dernier relevé</dt>
              <dd v-if="oldLastData(flowCaptData.lastdata)">
                {{ flowCaptData.lastdata }}
                <font-awesome-icon
                  id="lastDataIndicatorKo"
                  :style="{ color: 'red' }"
                  icon="times"
                />
              </dd>
              <dd v-else>
                {{ flowCaptData.lastdata }}
                <font-awesome-icon
                  id="lastDataIndicatorOk"
                  :style="{ color: 'green' }"
                  icon="check"
                />
              </dd>
            </dl>
            <b-tooltip target="lastDataIndicatorOk" placement="right">
              The capteur send his data at {{ flowCaptData.lastdata }}
            </b-tooltip>
            <b-tooltip target="lastDataIndicatorKo" placement="right">
              The capteur send his data more than 1 days ago at
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

export default {
  components: {
    FlowCaptMap,
    FlowCaptChart,
    BaseMap
  },
  async asyncData({ store, params }) {
    await store.dispatch('fetchFlowCaptStation')
    await store.dispatch('fetchFlowCaptData', params.id)
  },
  computed: {
    ...mapState(['flowCaptData', 'flowCaptStations']),
    selectedStation() {
      if (this.flowCaptData && this.flowCaptStations) {
        return this.flowCaptStations.features.find(
          (f) => this.flowCaptData.station === f.properties.fcs_id
        )
      } else {
        return null
      }
    }
  },
  methods: {
    oldLastData(dateAsStr) {
      return moment().diff(moment(dateAsStr), 'days') > 1
    }
  }
}
</script>
