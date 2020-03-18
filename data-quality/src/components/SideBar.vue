<template>
  <div class="side-bar-container">
    <ul>
      <li>
        <router-link to="/">Home</router-link> 
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data: () =>({
    name: ''
  }),
  methods: {
    goTo(route){
      this.$router.push({ name: route})
    }
  }
}
</script>

<style>

</style>