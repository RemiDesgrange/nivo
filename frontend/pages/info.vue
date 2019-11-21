<template>
  <div>
    <navbar />
    <alert-manager />
    <div class="container-fluid">
      Texte expplicatif de la démarche.
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'
import AlertManager from '@/components/alert/AlertManager'

export default {
  components: {
    Navbar,
    AlertManager
  }
}
</script>
