<template>
  <div class="detail">
    <h1 class="detail-title">Order detail</h1>

    <div class="detail-room">
      <p class="detail-room-text">Room:</p>
      <select class="detail-room-select" v-model="room_name">
        <option>101</option>
        <option>201</option>
        <option>301</option>
      </select>
    </div>

    <div class="detail-start">
      <p class="detail-start-text">Start at:</p>
      <input class="detail-start-select" type="datetime-local" v-model="start_time" />
    </div>

    <div class="detail-end">
      <p class="detail-end-text">End at:</p>
      <input class="detail-end-select" type="datetime-local" v-model="end_time" />
    </div>

    <button class="detail-button" @click="order_submit">Submit</button>

    <button class="detail-delete" @click="delete_submit">Delete this order</button>

    <p class="detail-message" v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'
import commons from '@/commons'

export default {
  created() {
    const getDetailOrder = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + VueCookies.get('access_token')
      }
    }

    fetch(commons.API_URL + '/room/order-detail/' + this.$route.params.idRoomOrder, getDetailOrder)
      .then(async response => {
        const data = await response.json()

        if (response.status === 404) {
          router.push('/order')
        } else if (response.status === 200) {
          this.room_name = data.room_order.room_name
          this.start_time = data.room_order.start_time.slice(0, 16)
          this.end_time = data.room_order.end_time.slice(0, 16)
        }
      })
  },
  data() {
    return {
      room_name: '',
      start_time: '',
      end_time: '',
      message: ''
    }
  },
  methods: {
    order_submit() {
      const editOrder = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + VueCookies.get('access_token')
        },
        body: JSON.stringify({
          room_name: this.room_name,
          start_time: this.start_time.replaceAll('T', ' '),
          end_time: this.end_time.replaceAll('T', ' ')
        })
      }

      fetch(commons.API_URL + '/room/order/' + this.$route.params.idRoomOrder, editOrder)
        .then(async response => {
          const data = await response.json()

          if (response.status === 401) {
            router.push('/login')
          } else {
            this.message = data.message
          }
        })
    },
    delete_submit() {
      const deleteOrder = {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + VueCookies.get('access_token')
        }
      }

      fetch(commons.API_URL + '/room/order/' + this.$route.params.idRoomOrder, deleteOrder)
        .then(async response => {
          const data = await response.json()

          if (response.status === 401) {
            router.push('/login')
          } else if (response.status === 400) {
            this.message = data.message
          } else {
            router.push('/order')
          }
        })
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Quicksand');

.detail {
  font-family: 'Quicksand', sans-serif;
  text-align: center;
  position: relative;
  height: 640px;
}

.detail-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.detail-room {
  position: absolute;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.detail-room-text {
  font-size: 20px;
  font-weight: 600;
}

.detail-room-select {
  width: 200px;
  height: 40px;
  padding-left: 40%;
  border-radius: 26px;
  border: none;
  outline: none;
  border: 1px solid green;
  font-size: 18px;
}

.detail-start {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  top: 200px;
}

.detail-start-text {
  font-size: 20px;
  font-weight: 600;
}

.detail-start-select {
  width: 250px;
  height: 40px;
  border-radius: 26px;
  padding-left: 80px;
  border: none;
  outline: none;
  padding-right: 10px;
  border: 1px solid green;
  font-size: 16px;
}

.detail-end {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  top: 320px;
}

.detail-end-text {
  font-size: 20px;
  font-weight: 600;
}

.detail-end-select {
  width: 250px;
  height: 40px;
  border-radius: 26px;
  padding-left: 80px;
  border: none;
  outline: none;
  padding-right: 10px;
  border: 1px solid green;
  font-size: 16px;
}

.detail-button {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 30px;
  border-radius: 24px;
  border: none;
  cursor: pointer;
  top: 480px;
}

.detail-button:hover {
  transition: 0.3s;
  background-color: green;
  color: white;
}

.detail-delete {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 30px;
  border-radius: 24px;
  border: none;
  cursor: pointer;
  top: 520px;
}

.detail-delete:hover {
  transition: 0.3s;
  background-color: red;
  color: white;
}

.detail-message {
  position: absolute;
  color: red;
  left: 50%;
  transform: translateX(-50%);
  font-size: 24px;
  font-weight: 600;
  top: 550px;
}
</style>
