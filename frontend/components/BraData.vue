<template>
  <div>
    <div v-if="braUrl">
      <div class="row my-3 justify-content-md-center">
        <b-col>
          <b-button-toolbar key-nav aria-label="Toolbar with button groups">
            <b-button-group class="mr-1">
              <b-button :disabled="noPrevious" :to="previousBraPath">
                Jour précédent
              </b-button>
              <b-button :disabled="noFollowed" :to="nextBraPath">
                Jour suivant
              </b-button>
            </b-button-group>
            <b-input-group class="mr1">
              <b-form-input
                :value="braDate"
                :debounce="1000"
                type="date"
                min="2016-03-10"
                @change="loadBraViaDatePicker"
              />
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
            des données liés à la neige, nous avons eu l'idée de rassembler ici
            les données qui nous semblaient pertinentes lors de la préparation
            de nos sorties.
          </p>
        </b-jumbotron>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  computed: {
    ...mapState(['braLoading', 'braData']),
    ...mapGetters(['braUrl', 'braDate']),
    noPrevious () {
      return !this.braData.previous_bra_id
    },
    noFollowed () {
      return !this.braData.next_bra_id
    },
    previousBraPath () {
      return `/bra/${this.$nuxt.context.params.massif}/${this.braData.previous_bra_id}`
    },
    nextBraPath () {
      return `/bra/${this.$nuxt.context.params.massif}/${this.braData.next_bra_id}`
    }
  },
  methods: {
    ...mapActions(['FETCH_BRA_DATA_BY_DATE']),
    async loadBraViaDatePicker (selectedDateAsString) {
      if (selectedDateAsString) {
        await this.FETCH_BRA_DATA_BY_DATE({ massif: this.braData.massif, date: selectedDateAsString })
      }
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
