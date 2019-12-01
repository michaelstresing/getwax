const profurl = "/profile"

var vm = new Vue({
  el: '#app',
  delimiters: ["[[","]]"],    // To prevent conflicts with vue syntax and jinja {{ }}
  vuetify: new Vuetify(),
  data: {
    name: '',
    picture: '',
    date: new Date().getFullYear() 
  },
  methods: {
    getprofile: function() {
      fetch(profurl)
      .then(
        function(response) {
          if (response.status !== 200) {
            console.log('Looks like there was a problem. Status Code: ' + response.status);
          }
          response.json().then(function(data) {
            console.log(data["name"]);
            vm.name = data["name"];
            console.log(data["picture"]);
            vm.picture = data["picture"];
          });
        }
      )}
    },

    // To run getprofile on loading of page.
    beforeMount(){
      vm.getprofile()
    }
  })

// To use FontAwesome icons. 
Vue.use(Vuetify, {
  iconfont: 'fa'
  })