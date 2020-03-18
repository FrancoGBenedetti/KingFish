<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <side-bar />
    <router-view/>
  </div>
</template>

<script>
import SideBar from './components/SideBar'
export default {
  data: () => ({
  }),
  components: {
    'side-bar': SideBar
  }
}
</script>

<style lang="less">

</style>
