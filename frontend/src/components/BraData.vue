<template>
  <div>
    <div class="row my-3 justify-content-md-center">
      <div class="col">
        <!-- TODO pagination -->
        <b-button-toolbar key-nav aria-label="Toolbar with button groups">
          <b-button-group class="mr-1">
            <b-button :disabled="noFollowed">&laquo;</b-button>
            <b-button :disabled="noFollowed">&lsaquo;</b-button>
          </b-button-group>
          <b-button-group class="mr-1">
            <b-button :disabled="noFollowed">Jour suivant</b-button>
            <b-button :disabled="noPrevious">Jour précédent</b-button>
          </b-button-group>
          <b-button-group class="mr-1">
            <b-button :disabled="noPrevious">&rsaquo;</b-button>
            <b-button :disabled="noPrevious">&raquo;</b-button>
          </b-button-group>
          <b-input-group class="mr1">
            <b-form-input :value="dateToday" type="date"></b-form-input>
          </b-input-group>
        </b-button-toolbar>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <b-embed
          id="bra-iframe"
          type="iframe"
          src="http://localhost:9000/bra/html/chablais/2019-01-01"
          aspect="1by1"
        ></b-embed>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      noPrevious: false,
      noFollowed: true,
      dateToday: '' //FIXME
    }
  }
}
</script>

<style>
#bra-iframe {
  width: 100%;
  position: absolute;
}
</style>
