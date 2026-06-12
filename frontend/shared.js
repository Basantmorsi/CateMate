// Shared CateMate frontend pieces, loaded via <script src="/shared.js"></script>
// after Vue + Vuetify. Each page builds Vuetify via cmVuetify() and registers
// the nav with:
//   const vuetify = cmVuetify()
//   createApp({...}).use(vuetify).component('app-nav', CmNav).mount('#app')

// The single source of truth for the app's palette. Edit colors here to
// restyle the whole app. Components reference `primary` / `secondary`,
// never literal color names.
function cmVuetify() {
  const { createVuetify } = Vuetify
  return createVuetify({
    theme: {
      defaultTheme: 'grape',
      themes: {
        grape: {
          dark: false,
          colors: {
            primary: '#6A1B9A',
            secondary: '#EC407A',
            surface: '#FFFFFF',
            background: '#F5F0F7',
          },
        },
      },
    },
  })
}

const CmNav = {
  // `current` is the page key so the nav can hide the link to the page you're on.
  // One of: home | browse | my-cats | liked | messages | login | register
  props: {
    current: { type: String, default: '' },
  },
  data() {
    return {
      loggedIn: !!localStorage.getItem('cm_token'),
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('cm_token')
      window.location.href = '/'
    },
  },
  template: `
    <v-app-bar color="primary" elevation="2">
      <v-app-bar-title>
        <a href="/" style="color:inherit;text-decoration:none;">
          <v-icon icon="mdi-cat" class="mr-2"></v-icon>CateMate
        </a>
      </v-app-bar-title>
      <template v-slot:append>
        <v-btn v-if="current !== 'browse'" href="/browse.html" variant="text" prepend-icon="mdi-magnify">Browse</v-btn>
        <template v-if="loggedIn">
          <v-btn v-if="current !== 'my-cats'" href="/my-cats.html" variant="text" prepend-icon="mdi-cat">My Cats</v-btn>
          <v-btn v-if="current !== 'liked'" href="/liked.html" variant="text" prepend-icon="mdi-heart">Liked</v-btn>
          <v-btn v-if="current !== 'messages'" href="/messages.html" variant="text" prepend-icon="mdi-email">Messages</v-btn>
          <v-btn @click="logout" variant="text" prepend-icon="mdi-logout">Logout</v-btn>
        </template>
        <template v-else>
          <v-btn v-if="current !== 'login'" href="/login.html" variant="text">Login</v-btn>
          <v-btn v-if="current !== 'register'" href="/register.html" variant="outlined" color="white" class="ml-2">Register</v-btn>
        </template>
      </template>
    </v-app-bar>
  `,
}
