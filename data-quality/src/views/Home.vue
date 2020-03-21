<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <table>
      <tr>
        <th>Company</th>
        <th>Contact</th>
        <th>Country</th>
      </tr>

    <template v-for="(tabla, idx) in tablas" >
     <tr  :key="idx">
        <td>{{tabla.columnas}}</td>
        <td>Maria Anders</td>
        <td>Germany</td>
      </tr>

    </template>

    </table>
    <Button text="Soy un botón"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import Button from '../components/Button.vue'
import validaciones from '../services/validaciones.js'
export default {
  name: 'Home',
  data:() =>({
    tablas:[]
  }),
  created(){
    validaciones.getTabla()
    .then(response=>{
      console.log(response)
      this.tablas = response
    })
    .catch(err => console.log(err))
  },
  components: {
    HelloWorld,
    Button
  }
}
</script>
