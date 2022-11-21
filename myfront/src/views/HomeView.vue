<template>
  <NavBar :fullName="full_name"></NavBar>
  <h1>{{ full_name }}</h1>
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  name: 'HomeView',
  components: {
    NavBar
  },
  data () {
    return {
      full_name: ''
    }
  },
  created () {
    const refreshToken = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        refresh: VueCookies.get('refresh_token')
      })
    }

    const getUserData = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + VueCookies.get('access_token')
      }
    }

    if (VueCookies.get('access_token') === null) {
      if (VueCookies.get('refresh_token') === null) {
        router.push('/login')
      } else {
        fetch('http://127.0.0.1:8000/authen/refresh-token', refreshToken)
          .then(async response => {
            const data = await response.json()

            if (response.status === 200) {
              VueCookies.set('access_token', data.access, 60 * 5)
              location.reload()
            } else {
              router.push('/login')
            }
          })
      }
    } else {
      fetch('http://127.0.0.1:8000/authen/login', getUserData)
        .then(async response => {
          const data = await response.json()

          if (response.status === 200) {
            this.full_name = data.full_name
          } else {
            router.push('/login')
          }
        })
    }
  }
}
</script>
