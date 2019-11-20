<template>
  <div id="app">
    <navbar />
    <alert-manager />
    <div class="container-fluid">
      <div class="row">
        <div class="col w-100">
          <h1>Station {{ flowCaptData.station }}</h1>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <flow-capt-chart />
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <flow-capt-map />
          </div>
          <div class="w-100"></div>
          <div class="col">
            <!-- <dl v-if="selectedStation">
              <dl>Station</dl>
              <dd>{{ selectedStation.properties.fcs_id }}</dd>
              <dl>label</dl>
              <dd>{{ selectedStation.properties.fcs_label }}</dd>
              <dl>pays</dl>
              <dd>{{ selectedStation.properties.fcs_country }}</dd>
              <dl></dl>
            </dl> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import FlowCaptChart from '@/components/chart/FlowCaptChart'

import Navbar from '@/components/Navbar'
import FlowCaptMap from '@/components/map/FlowCaptMap'
import AlertManager from '@/components/alert/AlertManager'

export default {
  components: {
    Navbar,
    AlertManager,
    FlowCaptMap,
    FlowCaptChart
  },
  computed: {
    ...mapState(['flowCaptData', 'flowCaptStations']),
    // selectedStation() {
    //   if (this.flowCaptData) {
    //     return this.flowCaptStations.features.filter(
    //       (f) => this.flowCaptData.station === f.properties.fcs_id
    //     )
    //   } else {
    //     return null
    //   }
    // }
  },
  async asyncData({ store, params }) {
    await store.dispatch('fetchFlowCaptStation')
    await store.dispatch('fetchFlowCaptData', params.flowcapt)
  }
}
</script>
