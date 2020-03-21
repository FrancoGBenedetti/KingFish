<template>
  <div class="home">
    <table class="table table-bordered">
    <thead>
      <tr>
        <th>First Name</th>
        <th>Last Name</th>
        <th>User ID</th>
      </tr>
    </thead>
    <tbody>
    <tr v-for="p in displayedPosts">
      <td>{{p.columna}}</td>
      <td>{{p.fila}}</td>
      <td>{{p.mensaje}}</td>
      <td>{{p.valor}}</td>
    </tr>
    </tbody>
  </table>
  <nav aria-label="Page navigation example">
			<ul class="pagination">
				<li class="page-item">
					<button type="button" class="page-link" v-if="page != 1" @click="page--"> Previous </button>
				</li>
				<li class="page-item">
					<button type="button" class="page-link" v-for="pageNumber in pages.slice(page-1, page+5)" @click="page = pageNumber"> {{pageNumber}} </button>
				</li>
				<li class="page-item">
					<button type="button" @click="page++" v-if="page < pages.length" class="page-link"> Next </button>
				</li>
			</ul>
		</nav>

    <Button text="Soy un botón"/>
  </div>
</template>

<script>
// @ is an alias to /src
import Button from '../components/Button.vue'
import validaciones from '../services/validaciones.js'
export default {
  name: 'Home',
  data:() =>({
    posts:[],
		page: 1,
		perPage: 9,
		pages: [],
  }),
  // created(){
  //   validaciones.getTabla()
  //   .then(response=>{
  //     console.log(response)
  //     this.filter(response, )
  //   })
  //   .catch(err => console.log(err))
  // },

  methods:{

  		setPages () {
  			let numberOfPages = Math.ceil(this.posts.length / this.perPage);
  			for (let index = 1; index <= numberOfPages; index++) {
  				this.pages.push(index);
  			}
  		},
  		paginate (posts) {
  			let page = this.page;
  			let perPage = this.perPage;
  			let from = (page * perPage) - perPage;
  			let to = (page * perPage);
  			return  posts.slice(from, to);
  		}
  	},
  	computed: {
  		displayedPosts () {
        console.log(this.paginate(this.posts))
  			return this.paginate(this.posts);
  		}
  	},
  	watch: {
  		posts () {
  			this.setPages();
  		}
  	},
  	created(){
      validaciones.getTabla()
      .then(response=>{
        this.posts = JSON.stringify(response)
        console.log('AQUI: ',this.posts)
      })
      .catch(err => console.log(err))
  	},
  	// filters: {
  	// 	trimWords(value){
  	// 		return value.split(" ").splice(0,20).join(" ") + '...';
  	// 	}
  	// }

}
</script>
