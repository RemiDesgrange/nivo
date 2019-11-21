<template>
  <div>
    <ul>
      <li v-for="record in nivoData" :v-if="nivoData">
        altitude : {{ record.haut_sta }} neige: {{ record.ht_neige * 100 }} cm
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['nivoData', 'nivoStations', 'selectedNivoStation'])
  }
}
</script>
