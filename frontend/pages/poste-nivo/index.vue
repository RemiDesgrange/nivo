<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <b-jumbotron>
            <h1>Données des poste des mesure du réseau nivo-météorologique</h1>
            <p class="lead">
              Ces données sont
              <a
                href="https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=94&id_rubrique=32"
              >
                issue de l'opendata
              </a>
              Météo France
            </p>
            <hr class="my-4" />
            <h3>Liste des stations</h3>
            <ul v-if="nivoStations" class="list-unstyled">
              <li
                v-for="station in nivoStations.features"
                :key="station.properties.nss_id"
              >
                <b-link
                  :to="'/poste-nivo/' + station.properties.nss_id"
                  @mouseover="showOverlay(station.properties.nss_id)"
                  @mouseleave="hideOverlay()"
                >
                  <!-- eslint-disable -->
                  <span class="capitalize"> {{ station.properties.nss_name | cleanStationsName }} </span>
                </b-link>
              </li>
            </ul>
          </b-jumbotron>
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <base-map>
              <nivo-map />
            </base-map>
          </div>
          <div class="w-100"></div>
          <div class="col"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import NivoMap from '~/components/map/NivoMap'
import BaseMap from '~/components/map/BaseMap'
import { gloablMutationTypes as types } from '@/modules/stateTypes'

export default {
  components: {
    NivoMap,
    BaseMap,
  },
  filters: {
    cleanStationsName(station) {
      return station.toLowerCase().replace('_', ' ')
    },
  },
  async asyncData({ store }) {
    await store.dispatch('fetchNivoStation')
  },
  computed: {
    ...mapState(['nivoStations']),
  },
  methods: {
    showOverlay(id) {
      this.$store.commit(
        types.SET_SELECTED_NIVO_STATION,
        this.nivoStations.features.find((n) => n.properties.nss_id === id)
      )
    },
    hideOverlay() {
      this.$store.commit(types.SET_SELECTED_NIVO_STATION, null)
    },
  },
}
</script>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>
