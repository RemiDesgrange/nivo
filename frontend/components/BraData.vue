<template>
  <div>
    <div v-if="braUrl">
      <div class="row my-3 justify-content-md-center">
        <b-col>
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
              <b-form-input :value="braDate" type="date"></b-form-input>
            </b-input-group>
          </b-button-toolbar>
        </b-col>
      </div>
      <b-row>
        <b-col>
          <b-overlay :show="braLoading">
            <b-embed
              id="bra-iframe"
              :src="braUrl"
              type="iframe"
              aspect="1by1"
            />
          </b-overlay>
        </b-col>
      </b-row>
    </div>
    <div v-else>
      <div class="container">
        <b-jumbotron>
          <template slot="header">
            Bienvenue sur Nivo !
          </template>
          <template slot="lead">
            Pour consulter les données d'un massifs, cliquez sur celui-ci dans
            la carte à droite.
          </template>

          <p>
            Frustré de l'ergonomie du site de météo france pour la consultation
            des données lié à la neige, nous avons eu l'idée de rassembler ici
            les données qui nous semblaient pertinentes lors de la préparation
            de nos sorties.
          </p>
        </b-jumbotron>
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
      noFollowed: true,
    }
  },
  computed: {
    ...mapState(['braLoading']),
    ...mapGetters(['braUrl', 'braDate']),
  },
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
