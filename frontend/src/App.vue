<template>
  <div id="app">
    <navbar />
    <div class="container-fluid">
      <div class="row">
        <div class="col-6">
          <bra-data />
        </div>
        <div class="col-6">
          <ign-map />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import IgnMap from "./components/IgnMap";
import Navbar from "./components/Navbar";
import BraData from "./components/BraData";

export default {
  name: "app",
  components: {
    Navbar,
    IgnMap,
    BraData
  }
};
</script>
