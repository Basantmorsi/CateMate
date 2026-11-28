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
  // One of: home | browse | my-cats | liked | messages | profile | login | register
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
          <v-btn v-if="current !== 'profile'" href="/profile.html" variant="text" prepend-icon="mdi-account-circle">Profile</v-btn>
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

// Map picker (Leaflet + OpenStreetMap, no API key). Load Leaflet's CSS and JS
// before this file on pages that use it.
//
//   const picker = cmLocationPicker('map', {
//     lat, lng,            // current pin, or null for none
//     cityLat, cityLng,    // centre used when there is no pin
//     onChange(lat, lng),  // called with the pin rounded to 2 decimals (~1 km)
//     readonly: false,     // true = preview only, no clicking or dragging
//   })
//   picker.setPin(lat, lng)      // move the pin (null, null removes it)
//   picker.setCity(lat, lng)     // re-centre the map without a pin
//   picker.invalidate()          // call after the map's container becomes visible
//   picker.destroy()             // call before the map's element is removed
const CM_LOCATION_HINT = 'Pick a spot near you, not your exact address. Other owners will only see an approximate distance.'

function cmRound2(value) {
  return Math.round(value * 100) / 100
}

function cmLocationPicker(elementId, options) {
  const { lat, lng, cityLat, cityLng, onChange, readonly } = options
  const hasPin = lat != null && lng != null
  const start = hasPin ? [lat, lng] : (cityLat != null ? [cityLat, cityLng] : [50.5, 10])
  const zoom = hasPin || cityLat != null ? 11 : 4

  const map = L.map(elementId, {
    dragging: true,
    scrollWheelZoom: !readonly,
  }).setView(start, zoom)
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map)

  let marker = null
  function place(la, ln, notify) {
    const r = [cmRound2(la), cmRound2(ln)]
    if (!marker) {
      marker = L.marker(r, { draggable: !readonly }).addTo(map)
      if (!readonly) {
        marker.on('dragend', () => {
          const p = marker.getLatLng()
          place(p.lat, p.lng, true)
        })
      }
    } else {
      marker.setLatLng(r)
    }
    if (notify && onChange) onChange(r[0], r[1])
  }

  if (hasPin) place(lat, lng, false)
  if (!readonly) map.on('click', e => place(e.latlng.lat, e.latlng.lng, true))

  return {
    setPin(la, ln) {
      if (la == null || ln == null) {
        if (marker) { marker.remove(); marker = null }
        return
      }
      place(la, ln, false)
      map.setView([la, ln], map.getZoom())
    },
    setCity(la, ln) {
      if (la != null && ln != null) map.setView([la, ln], 11)
    },
    invalidate() { map.invalidateSize() },
    destroy() { map.remove() },
  }
}
