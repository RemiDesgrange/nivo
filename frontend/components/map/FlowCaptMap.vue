<template>
  <div>
    <div v-if="SELECTED_FLOWCAPT_STATION_CLICK.length > 0">
      <ol-overlay
        v-for="feature in SELECTED_FLOWCAPT_STATION_CLICK"
        :id="'flowcapt-popup-' + feature.get('id')"
        :key="feature.id"
        :position="feature"
        class="feature-popup"
      >
        <b-card :title="'Site ' + feature.get('fcs_site')">
          <b-card-text>
            <ul>
              <li><em>Identifiant</em> : {{ feature.get('fcs_id') }}</li>
              <li><em>Site</em> : {{ feature.get('fcs_site') }}</li>
              <li><em>Pays</em> : {{ feature.get('fcs_country') }}</li>
              <li><em>Altitude</em> : {{ feature.get('fcs_altitude') }}</li>
            </ul>
          </b-card-text>
          <b-button :to="'/flowcapt/' + feature.get('fcs_id')">
            voir les données
          </b-button>
        </b-card>
      </ol-overlay>
    </div>
    <div v-else>
      <ol-overlay
        v-for="feature in SELECTED_FLOWCAPT_STATION_HOVER"
        :id="'flowcapt-popup-' + feature.get('id')"
        :key="feature.id"
        :position="feature"
        class="feature-popup"
      >
        <b-card :title="'Site ' + feature.get('fcs_site')">
          <b-card-text>
            <ul>
              <li><em>Identifiant</em> : {{ feature.get('fcs_id') }}</li>
              <li><em>Site</em> : {{ feature.get('fcs_site') }}</li>
              <li><em>Pays</em> : {{ feature.get('fcs_country') }}</li>
              <li><em>Altitude</em> : {{ feature.get('fcs_altitude') }}</li>
            </ul>
          </b-card-text>
        </b-card>
      </ol-overlay>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import OlOverlay from '~/components/map/overlay/OlOverlay'
import { mapGettersTypes as getterTypes } from '~/modules/stateTypes'

export default {
  components: {
    OlOverlay,
  },
  computed: {
    ...mapGetters('map', [
      getterTypes.SELECTED_FLOWCAPT_STATION_HOVER,
      getterTypes.SELECTED_FLOWCAPT_STATION_CLICK,
    ]),
  },
}
</script>
