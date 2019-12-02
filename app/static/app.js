const profurl = "/profile"

// Setting custom color scheme
const mainvuetify = new Vuetify({
    themes: {
      dark: {
        primary: '#16161A',
        accent: '#FFFFFE',
        secondary: '#7F5AF0',
        success: '#4CAF50',
        info: '#2CB67D',
        warning: '#FFEF61',
        error: '#7D0000'
      }
    },
  })

Vue.use(mainvuetify)

var vm = new Vue({
  el: '#app',
  delimiters: ["[[","]]"],    // To prevent conflicts with vue syntax and jinja {{ }}
  vuetify: mainvuetify,
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
    // beforeMount(){
    //   vm.getprofile()
    // }
  })

// To use FontAwesome icons. 
Vue.use(Vuetify, {
  iconfont: 'fa'
  })