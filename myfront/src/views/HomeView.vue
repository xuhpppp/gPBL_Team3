<template>
  <NavBar :fullName="full_name"></NavBar>
  <RoomCondition :roomCondition="room_condition"></RoomCondition>
  <OptionMenu :isAdmin="is_admin"></OptionMenu>
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
import RoomCondition from '@/components/RoomCondition.vue'
import OptionMenu from '@/components/OptionMenu.vue'
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  name: 'HomeView',
  components: {
    NavBar,
    RoomCondition,
    OptionMenu
  },
  data () {
    return {
      full_name: '',
      is_admin: false,
      room_condition: []
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

    const getHomeData = {
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
      fetch('http://127.0.0.1:8000/authen/login', getHomeData)
        .then(async response => {
          const data = await response.json()

          if (response.status === 200) {
            this.full_name = data.full_name
            this.is_admin = data.is_admin
          } else {
            router.push('/login')
          }
        })

      fetch('http://127.0.0.1:8000/room/order', getHomeData)
        .then(async response => {
          const data = await response.json()

          if (response.status === 200) {
            this.room_condition = data.room_condition
          } else {
            router.push('/login')
          }
        })
    }
  }
}
</script>

<style scoped>
  @media (max-width: 1280px) {
    body {
      background-color: white;
      background-image: none;
    }
  }
</style>
