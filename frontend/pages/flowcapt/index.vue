<template>
  <div id="app">
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-6 col-md-12 col-sm-12">
          <b-jumbotron>
            <h1>Données Station de mesure FlowCapt</h1>
            <p class="lead">
              Ces données sont représenté avec l'aimable autorisation de ISAW.
              Aucune garantie quand à la fiabilité de ces données ne peux être
              garantie.
            </p>
            <hr class="my-4" />
            <h3>Liste des stations</h3>
            <ul v-if="flowCaptStations" class="list-unstyled">
              <li
                v-for="station in flowCaptStations.features"
                :key="station.properties.fcs_id"
              >
                <b-link :to="'/flowcapt/' + station.properties.fcs_id">
                  {{ station.properties.fcs_site }},
                  <strong>{{ station.properties.fcs_id }}</strong>
                </b-link>
              </li>
            </ul>
          </b-jumbotron>
        </div>
        <div class="col-lg-6 col-md-12 col-sm-12">
          <div class="col">
            <base-map>
              <flow-capt-map />
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
import FlowCaptMap from '@/components/map/FlowCaptMap'
import BaseMap from '@/components/map/BaseMap'

export default {
  components: {
    FlowCaptMap,
    BaseMap
  },
  async asyncData({ store }) {
    await store.dispatch('fetchFlowCaptStation')
  },
  computed: mapState(['flowCaptStations'])
}
</script>
