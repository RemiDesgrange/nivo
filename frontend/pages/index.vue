<template>
  <div id="app">
    <navbar />
    <b-alert :show="errors.length > 0" dismissible variant="danger">
      <p>{{ errors }}</p>
    </b-alert>
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
import { mapState } from 'vuex'
import BaseMap from '@/components/BaseMap'
import Navbar from '@/components/Navbar'
import BraData from '@/components/BraData'
import NivoData from '@/components/NivoData'

export default {
  components: {
    Navbar,
    BaseMap,
    BraData,
    NivoData
  },
  computed: mapState(['errors']),
  async asyncData({ store, params }) {
    await store.dispatch('fetchMassifs')
    await store.dispatch('fetchNivoseStation')
  }
}
</script>
