<template>
  <div>
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
        :display-link="false"
      />
    </ol-overlay>
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
    BraOverlay
  },
  computed: {
    ...mapState('map', ['massifs']),
    ...mapGetters('map', [mapGettersTypes.SELECTED_MASSIF_HOVER])
  }
}
</script>

<style></style>
