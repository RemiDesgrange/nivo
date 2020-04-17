<template>
  <div>
    <!--      <vl-layer-vector id="flowCaptStationLayer" render-mode="image">-->
    <!--        &lt;!&ndash; <vl-style-func :factory="myStyleFunc" /> &ndash;&gt;-->
    <!--        <vl-source-vector-->
    <!--          :v-if="flowCaptStations"-->
    <!--          :features="flowCaptStations.features"-->
    <!--        ></vl-source-vector>-->
    <!--        &lt;!&ndash; <vl-style-box>-->
    <!--          <vl-style-circle :radius="5">-->
    <!--            <vl-style-stroke color="white"></vl-style-stroke>-->
    <!--            <vl-style-fill color="red"></vl-style-fill>-->

    <!--          </vl-style-circle>-->
    <!--        </vl-style-box> &ndash;&gt;-->
    <!--      </vl-layer-vector>-->
    <!-- get all selection event. This up to us to handle everything and dispatch -->
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
        <b-button :to="'/flowcapt/' + feature.get('fcs_id')">
          voir les données
        </b-button>
      </b-card>
    </ol-overlay>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import OlOverlay from '~/components/map/OlOverlay'
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

<style>
#vl-map-map {
  width: 100%;
  height: 500px;
}
</style>
