<template>
  <div>
    <navbar />
    <alert-manager />
    <nuxt />
  </div>
</template>

<script>
import AlertManager from '@/components/alert/AlertManager'
import Navbar from '@/components/Navbar'

export default {
  components: {
    AlertManager,
    Navbar
  }
}
</script>
