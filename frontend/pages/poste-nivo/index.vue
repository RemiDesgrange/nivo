<template>
  <div>
    <navbar />
    <alert-manager />
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
            <ul class="list-unstyled">
              <li v-for="station in nivoStations.features" v-if="nivoStations">
                <b-link :to="'/poste-nivo/' + station.properties.nss_id">
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
import Navbar from '@/components/Navbar'
import AlertManager from '@/components/alert/AlertManager'
import NivoMap from '@/components/map/NivoMap'
import BaseMap from '@/components/map/BaseMap'

export default {
  components: {
    Navbar,
    AlertManager,
    NivoMap,
    BaseMap
  },
  filters: {
    cleanStationsName(station) {
      return station.toLowerCase().replace('_', ' ')
    }
  },
  computed: {
    ...mapState(['nivoStations'])
  },
  async asyncData({ store }) {
    await store.dispatch('fetchNivoStation')
  }
}
</script>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>
