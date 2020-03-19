<template>
  <div id="app">
    // BARRA DE NAVEGACION
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    //BARRA DE NAVEGACION
    <div class="main-layout">

      <div class="side-bar">
        <side-bar />
      </div>

      <div class="content">
        <router-view/>
      </div>

    </div>

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
@primary-color: red;
.main-layout{
  display: flex;
  .content{
    background-color: @primary-color;
  }
}

</style>
