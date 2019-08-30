<template>
  <div id="app">
    <navbar />
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <bra-data />
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <ign-map />
          </div>
          <div class="w-100"></div>
          <div class="col">
            <nivo-data />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import IgnMap from './components/IgnMap'
import Navbar from './components/Navbar'
import BraData from './components/BraData'
import NivoData from './components/NivoData'

export default {
  name: 'app',
  components: {
    Navbar,
    IgnMap,
    BraData,
    NivoData
  }
}
</script>
