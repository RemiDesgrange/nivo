<template>
  <div v-if="braUrl">
    <div class="row my-3 justify-content-md-center">
      <div class="col">
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
            <b-form-input value="01/01/2019" type="date"></b-form-input>
          </b-input-group>
        </b-button-toolbar>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <b-spinner
          v-if="massifLoading"
          type="grow"
          label="Spinning"
        ></b-spinner>
        <b-embed
          id="bra-iframe"
          type="iframe"
          :src="braUrl"
          aspect="1by1"
        ></b-embed>
      </div>
    </div>
  </div>
</template>
<script>
import { mapState, mapGetters } from 'vuex'

export default {
  data() {
    return {
      noPrevious: false,
      noFollowed: true
    }
  },
  computed: {
    ...mapState(['massifLoading']),
    ...mapGetters(['braUrl'])
  },
  methods: {
    getMassifsFeature(featureCollection) {
      if (featureCollection) {
        return featureCollection.features
      }
      return []
    }
  }
}
</script>

<style scoped>
#bra-iframe {
  width: 100%;
  position: absolute;
}
.captialize-text {
  text-transform: capitalize;
}
</style>
