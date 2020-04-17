<template>
  <div>
    <!-- nivo station -->
    <ol-overlay
      v-for="feature in SELECTED_NIVO_STATION_HOVER"
      :id="'nivo-stations-popover-' + feature.getId()"
      :key="feature.getId()"
      :position="feature"
      class="feature-popup"
    >
      <b-card>
        <b-card-title class="capitalize">
          Site {{ feature.get('nss_name').toLowerCase() }}
        </b-card-title>
        <b-card-text>
          <ul>
            <li>
              <em>Altitude</em>
              {{ feature.getGeometry().getCoordinates().pop() }}
            </li>
            <li>
              <em>Identifiant Météo France</em>
              <span class="capitalize">{{
                feature.get('nss_meteofrance_id')
              }}</span>
            </li>
          </ul>
        </b-card-text>
        <b-button :to="'/poste-nivo/' + feature.get('nss_id')">
          voir les données
        </b-button>
      </b-card>
    </ol-overlay>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import OlOverlay from '~/components/map/OlOverlay'
import { mapGettersTypes } from '~/modules/stateTypes'

export default {
  components: {
    OlOverlay,
  },
  computed: {
    ...mapState(['nivoStations', 'selectedNivoStation']),
    ...mapGetters('map', [
      mapGettersTypes.SELECTED_NIVO_STATION_HOVER,
      mapGettersTypes.SELECTED_NIVO_STATION_CLICK,
    ]),
  },
}
</script>
<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>
