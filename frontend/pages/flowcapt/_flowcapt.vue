<template>
  <div id="app">
    <navbar />
    <alert-manager />
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <flow-capt-chart />
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <flow-capt-map />
          </div>
          <div class="w-100"></div>
          <div class="col"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
  async asyncData({ store, params }) {
    await store.dispatch('fetchFlowCaptStation')
    await store.dispatch('fetchFlowCaptData', params.flowcapt)
  }
}
</script>
