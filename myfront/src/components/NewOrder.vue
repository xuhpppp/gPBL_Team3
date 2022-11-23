<template>
    <div class="new">
        <div class="new-form">
            <h1 class="new-form-title">New order</h1>

            <div class="new-form-room">
                <p class="new-form-room-text">Room:</p>
                <select class="new-form-room-select" v-model="room_name">
                    <option>101</option>
                    <option>201</option>
                    <option>301</option>
                </select>
            </div>

            <div class="new-form-start">
                <p class="new-form-start-text">Start at:</p>
                <input class="new-form-start-select" type="datetime-local" v-model="start_time"/>
            </div>

            <div class="new-form-end">
                <p class="new-form-end-text">End at:</p>
                <input class="new-form-end-select" type="datetime-local" v-model="end_time"/>
            </div>

            <button class="new-form-button" @click="order_submit">Submit</button>

            <p class="new-form-message" v-if="message">{{message}}</p>
        </div>
    </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  data () {
    return {
      room_name: '',
      start_time: '',
      end_time: '',
      message: '',
      new_order: {
        user: 'a',
        room_name: this.room_name,
        start_time: this.start_time,
        end_time: this.end_time
      }
    }
  },
  methods: {
    order_submit () {
      const createOrder = {
        method: 'POST',
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

      fetch('http://127.0.0.1:8000/room/order', createOrder)
        .then(async response => {
          const data = await response.json()

          if (response.status === 401) {
            router.push('/login')
          } else {
            this.message = data.message

            // emit to update real-time
            this.new_order.user = data.full_name
            this.new_order.room_name = this.room_name
            this.new_order.start_time = this.start_time
            this.new_order.end_time = this.end_time
            this.$emit('inputData', this.new_order)
          }
        })
    }
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  .new {
    font-family: 'Quicksand', sans-serif;
    position: relative;
    height: 600px;
    margin-top: 20px;
  }

  .new-form {
    position: absolute;
    display: flex;
    flex-direction: column;
    width: 70%;
    left: 50%;
    transform: translateX(-50%);
    flex-wrap: wrap;
    align-items: center;
    border-radius: 26px;
  }

  .new-form-title {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  .new-form-room {
    position: absolute;
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
  }

  .new-form-room-text {
    font-size: 20px;
    font-weight: 600;
  }

  .new-form-room-select {
    width: 200px;
    height: 40px;
    padding-left: 40%;
    border-radius: 26px;
    border: none;
    outline: none;
    border: 1px solid green;
    font-size: 18px;
  }

  .new-form-start {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    top: 200px;
  }

  .new-form-start-text {
    font-size: 20px;
    font-weight: 600;
  }

  .new-form-start-select {
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

  .new-form-end {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    top: 320px;
  }

  .new-form-end-text {
    font-size: 20px;
    font-weight: 600;
  }

  .new-form-end-select {
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

  .new-form-button {
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

  .new-form-button:hover {
    transition: 0.3s;
    background-color: green;
    color: white;
  }

  .new-form-message {
    position: absolute;
    color: red;
    left: 50%;
    transform: translateX(-50%);
    font-size: 24px;
    font-weight: 600;
    top: 500px;
  }
</style>
