<template>
  <div :id="id">
    <slot />
  </div>
</template>

<script>
import Overlay from 'ol/Overlay'
import Feature from 'ol/Feature'
import { findPointOnSurface } from '~/modules/mapUtils'

export default {
  props: {
    position: {
      type: Feature,
      required: true
    },
    id: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      overlay: new Overlay({
        autoPan: true,
        autoPanAnimation: false,
        positioning: 'center-right'
      })
    }
  },
  mounted () {
    this.overlay.setElement(document.getElementById(this.id))
    this.overlay.setPosition(findPointOnSurface(this.position.getGeometry()))
    this.$store.commit('map/ADD_OVERLAY', this.overlay)
  },
  beforeDestroy () {
    this.$store.commit('map/REMOVE_OVERLAY', this.overlay)
  }
}
</script>
