<template>
  <div class="container-fluid">
    <!--<div class="row">-->
    <navbar></navbar>
    <!--</div>-->
    <div class="row">
      <div class="col-6">
        <bra-data></bra-data>
      </div>
      <div class="col-6">
        <massif-map></massif-map>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar'
import BraData from './BraData'
import MassifMap from './MassifMap'

export default {
  components: {
    navbar: Navbar,
    'bra-data': BraData,
    'massif-map': MassifMap
  }
}
</script>
