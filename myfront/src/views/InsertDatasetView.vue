<template>
    <div class="new">
        <h1 class="new-title">Insert new dataset system</h1>

        <p class="new-subscription">Slowly move your face around the webcam for about 15 seconds, remember that only your face appears in front of the webcam</p>

        <img class="new-img" src="../assets/face-scan.png" alt="">

        <button class="new-btn" @click="startScanning">Start</button>
    </div>

    <div class="time">{{ time_left }}</div>

    <div class="message">{{ message }}</div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  data () {
    return {
      message: '',
      time_left: 15,
      id: ''
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
    }
  },
  methods: {
    startScanning () {
      document.getElementsByClassName('time')[0].style.opacity = '1'

      const socket = new WebSocket('ws://localhost:8000/ws/insert')

      socket.onmessage = function (event) {
        var data = JSON.parse(event.data)

        self.message = data.message

        socket.close()
      }

      const self = this
      // countdown 15sec to close socket
      const timer = setInterval(countDown, 1000)

      function countDown () {
        if (self.time_left > 0) {
          self.time_left -= 1
        } else {
          clearInterval(timer)

          const getHomeData = {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + VueCookies.get('access_token')
            }
          }
          fetch('http://127.0.0.1:8000/authen/login', getHomeData)
            .then(async response => {
              const dataReceived = await response.json()

              if (response.status === 200) {
                self.message = 'Please wait...'
                socket.send(dataReceived.id)
              } else {
                router.push('/')
              }
            })

          self.time_left = 15
        }
      }
    }
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  .new {
    font-family: 'Quicksand', sans-serif;
    background-color: white;
    width: 60%;
    border-radius: 26px;
    display: flex;
    flex-direction: column;
    align-items: center;
    left: 50%;
    position: relative;
    transform: translateX(-50%);
    margin-top: 30px;
    padding-bottom: 40px;
    padding-left: 60px;
    padding-right: 60px;
  }

  .new-img {
    width: 300px;
  }

  .new-btn {
    width: 200px;
    height: 40px;
    border: 1px solid green;
    background-color: transparent;
    border-radius: 24px;
    cursor: pointer;
  }

  .new-btn:hover {
    transition: 0.3s;
    background-color: green;
    color: white;
  }

  .time {
    font-family: 'Quicksand', sans-serif;
    font-weight: 600;
    font-size: 30px;
    text-align: center;
    opacity: 0;
    margin-top: 30px;
  }

  .message {
    font-family: 'Quicksand', sans-serif;
    font-size: 22px;
    color: red;
    text-align: center;
    margin-top: 30px;
  }
</style>
