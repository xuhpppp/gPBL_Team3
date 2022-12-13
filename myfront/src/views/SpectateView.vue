<template>
  <div class="select">
    <div class="select-element active" @click="change_active('101')">101</div>

    <div class="select-element" @click="change_active('201')">201</div>

    <div class="select-element" @click="change_active('301')">301</div>
  </div>

  <div class="stream">
    <img :src="main_link" alt="" class="stream-screen">
  </div>

  <div class="info">
    <!-- dev here... -->
  </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'
import commons from '@/commons'

export default {
  data() {
    return {
      link: ['', 'https://floridahsfootball.com/wp-content/uploads/2016/10/IMG-Academy-Featured.png', 'https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_1295,h_720/w_80,x_15,y_15,g_south_west,l_Klook_water_br_trans_yhcmh3/activities/t9ur9cc1khkup1dmcbzd/V%C3%A9C%C3%B4ngVi%C3%AAnGi%E1%BA%A3iTr%C3%ADIMGWorldsofAdventure.jpg'],
      main_link: ''
    }
  },
  created() {
    const refreshToken = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        refresh: VueCookies.get('refresh_token')
      })
    }

    const checkAdmin = {
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
        fetch(commons.API_URL + '/authen/refresh-token', refreshToken)
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
      fetch(commons.API_URL + '/authen/admin', checkAdmin)
        .then(async response => {
          const data = await response.json()

          if (response.status === 401) {
            router.push('/')
          } else {
            this.main_link = data.link_101
            this.link[0] = data.link_101
          }
        })
    }
  },
  methods: {
    change_active(roomName) {
      const div = document.getElementsByClassName('select-element')

      for (let i = 0; i < div.length; i++) {
        if (div[i].innerHTML === roomName) {
          div[i].classList.add('active')

          this.main_link = this.link[i]
        } else {
          div[i].classList.remove('active')
        }
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Quicksand');

.select {
  font-family: 'Quicksand', sans-serif;
  position: relative;
  display: flex;
  width: 70%;
  justify-content: space-around;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 30px;
}

.select-element {
  background-color: white;
  border-radius: 26px;
  width: 200px;
  height: 40px;
  font-size: 24px;
  text-align: center;
  padding-top: 10px;
  cursor: pointer;
}

.select-element:hover {
  transition: 0.3s;
  background-color: green;
  color: white;
}

.active {
  background-color: green;
  color: white;
}

.stream {
  position: relative;
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.stream-screen {
  width: 70%;
  border: 3px solid #4caf45;
  border-radius: 16px;
}
</style>
