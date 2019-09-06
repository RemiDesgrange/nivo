<template>
  <div id="app">
    <navbar />
    <alert-manager />
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <bra-data />
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <base-map />
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
import BaseMap from '@/components/map/BaseMap'
import Navbar from '@/components/Navbar'
import BraData from '@/components/BraData'
import NivoData from '@/components/NivoData'
import AlertManager from '@/components/alert/AlertManager'

export default {
  components: {
    Navbar,
    BaseMap,
    BraData,
    NivoData,
    AlertManager
  }
}
</script>
