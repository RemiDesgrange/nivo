<template>
  <div>
    <!-- This is a ugly solution to keep having the overlay while not hovering the massif.-->
    <div v-if="SELECTED_MASSIF_CLICK.length > 0">
      <ol-overlay
        v-for="feature in SELECTED_MASSIF_CLICK"
        :id="'popup-massif-hover' + feature.get('id')"
        :key="feature.id"
        class="massifHover"
        :position="feature"
      >
        <bra-overlay
          :name="feature.get('name')"
          :bradata="feature.get('latest_record')"
          :displayLink="true"
        />
      </ol-overlay>
    </div>
    <div v-else>
      <ol-overlay
        v-for="feature in SELECTED_MASSIF_HOVER"
        :id="'popup-massif-hover' + feature.get('id')"
        :key="feature.id"
        class="massifHover"
        :position="feature"
      >
        <bra-overlay
          :name="feature.get('name')"
          :bradata="feature.get('latest_record')"
          :displayLink="false"
        />
      </ol-overlay>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import OlOverlay from './overlay/OlOverlay'
import BraOverlay from './overlay/BraOverlay'
import { mapGettersTypes } from '~/modules/stateTypes'

export default {
  components: {
    OlOverlay,
    BraOverlay,
  },
  computed: {
    ...mapState('map', ['massifs']),
    ...mapGetters('map', [
      mapGettersTypes.SELECTED_MASSIF_CLICK,
      mapGettersTypes.SELECTED_MASSIF_HOVER,
    ]),
  },
}
</script>

<style></style>
