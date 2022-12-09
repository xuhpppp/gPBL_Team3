<template>
    <div class="checkin">
      <div class="checkin-status">
        <h1 class="checkin-status-title">Auto check-in system</h1>

        <h2 class="checkin-status-user" v-for="user in online_users" :key="user">{{ user }}</h2>
      </div>

      <div class="checkin-bar">
        <div class="checkin-bar-progress"></div>
      </div>

      <h2 class="checkin-message">{{ message }}</h2>

      <h2 class="checkin-next" v-if="next_order !== 'There is no order!'">The next order: {{ next_order.start_time.replace('T', ' ').slice(0, 16) }} to {{ next_order.end_time.replace('T', ' ').slice(0, 16) }}</h2>
      <h2 class="checkin-next" v-else>The next order: {{ next_order }}</h2>
    </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  data () {
    return {
      online_users: [],
      next_order: '',
      recognize_process: 0,
      message: ''
    }
  },
  created () {
    let checkInAPI = 0

    const refreshToken = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        refresh: VueCookies.get('refresh_token')
      })
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
      const socket = new WebSocket('ws://localhost:8000/ws/some_url')

      const self = this
      socket.onmessage = function (event) {
        var data = JSON.parse(event.data)

        if (self.online_users.length > 0 && self.online_users.length === data.online_users.length) {
          let diffFlag = 0

          for (let i = 0; i < self.online_users.length; i++) {
            if (!data.online_users.includes(self.online_users[i])) {
              diffFlag = 1
            }
          }
          for (let i = 0; i < data.online_users.length; i++) {
            if (!self.online_users.includes(data.online_users[i])) {
              diffFlag = 1
            }
          }

          if (diffFlag === 1) {
            self.recognize_process = 0
            checkInAPI = 0
          } else {
            if (self.recognize_process < 100) {
              self.recognize_process += 1

              document.getElementsByClassName('checkin-bar-progress')[0].style.width = self.recognize_process + '%'
            } else if (self.recognize_process === 100 && checkInAPI === 0) {
              let nextOrderId = 0
              if (self.next_order.id != null) {
                nextOrderId = self.next_order.id
              }

              const checkIn = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  online_users: self.online_users,
                  roomOrder_id: nextOrderId
                })
              }

              fetch('http://127.0.0.1:8000/face/check-in', checkIn)
                .then(async response => {
                  const data = await response.json()

                  self.message = data.message
                })

              checkInAPI = 1
            }
          }
        } else {
          self.recognize_process = 0
          checkInAPI = 0
        }

        self.online_users = data.online_users
        if (data.next_order != null) {
          self.next_order = data.next_order
        }
      }
    }
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  .checkin {
    font-family: 'Quicksand', sans-serif;
    position: relative;
  }

  .checkin-status {
    position: absolute;
    width: 50%;
    background-color: white;
    border-radius: 24px;
    height: 400px;
    text-align: center;
    left: 50%;
    transform: translateX(-50%);
  }

  .checkin-bar {
    width: 600px;
    height: 30px;
    border: 1px solid white;
    border-radius: 20px;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 450px;
  }

  .checkin-bar-progress {
    width: 0%;
    height: 100%;
    background-color: green;
    border-radius: 20px;
  }

  .checkin-message {
    color: red;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 520px;
  }

  .checkin-next {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 570px;
  }
</style>
