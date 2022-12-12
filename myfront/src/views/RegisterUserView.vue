<template>
    <div class="box">
        <h1 class="box-title">Register a new user</h1>

        <input class="box-input" type="text" placeholder="Full name..." v-model="full_name">

        <input class="box-input" type="email" placeholder="Email..." v-model="email">

        <input class="box-input" type="password" placeholder="Password..." v-model="password">

        <input class="box-input" type="password" placeholder="Re-enter password..." v-model="re_password">

        <label class="box-label">Admin</label>
        <input class="box-select" type="checkbox" v-model="is_admin">

        <button class="box-button" @click="register">Register</button>
    </div>

    <p class="message">{{ message }}</p>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  data () {
    return {
      message: '',
      email: '',
      full_name: '',
      password: '',
      re_password: '',
      is_admin: false
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
    register () {
      const RegisterRequest = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.email,
          full_name: this.full_name,
          password: this.password,
          re_password: this.re_password,
          is_admin: this.is_admin
        })
      }

      fetch('http://127.0.0.1:8000/authen/register', RegisterRequest)
        .then(async response => {
          const data = await response.json()
          console.log(data.message)
          this.message = data.message
        })
    }
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  .box {
    font-family: 'Quicksand', sans-serif;
    background-color: white;
    width: 60%;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 26px;
    display: flex;
    flex-direction: column;
    text-align: center;
    margin-top: 5%;
    height: 500px;
  }

  .box-title {
    margin-top: 50px;
    margin-bottom: 40px;
  }

  .box-input {
    position: relative;
    width: 30%;
    left: 50%;
    transform: translateX(-50%);
    height: 30px;
    border-radius: 24px;
    border: 1px solid #57bb55;
    outline: none;
    padding-left: 20px;
    margin-top: 16px;
  }

  .box-input:hover {
    transition: 0.3s;
    border-color: green;
  }

  .box-input:focus {
    transition: 0.3s;
    border-width: 2px;
  }

  .box-button {
    width: 100px;
    height: 30px;
    border: 1px solid gray;
    cursor: pointer;
    border-radius: 20px;
    background-color: white;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 40px;
  }

  .box-button:hover {
    transition: 0.3s;
    border: 1px solid green;
    background-color: green;
    color: white;
  }

  .box-label {
    margin-top: 30px;
  }

  .message {
    position: relative;
    color: red;
    font-size: 20px;
    margin-top: 50px;
    font-family: 'Quicksand', sans-serif;
    text-align: center;
  }
</style>
