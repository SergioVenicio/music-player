<template>
  <div id="app">
    <div>
      <app-header></app-header>
    </div>
    <router-view/>
  </div>
</template>

<script>
import Header from './components/Header'
export default {
  name: 'Music-Player',
  components: {
    'app-header': Header
  }
}
</script>

<style scoped>
</style>
