<template>
    <div class="login">
        <img class="login-img" src="../assets/icon_png.png" alt="">

        <h1 class="login-title">LOGIN</h1>

        <div class="login-input">
            <input class="login-input-email" type="text" placeholder="Type your email..." v-model="email">
            <input class="login-input-password" type="password" placeholder="Type your password..." v-model="password">

            <button class="login-input-button" @click="login_submit">Login</button>
        </div>
    </div>
</template>

<script>
import VueCookies from 'vue-cookies'

export default {
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    login_submit () {
      const LoginRequest = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.email,
          password: this.password
        })
      }

      fetch('http://127.0.0.1:8000/authen/login', LoginRequest)
        .then(async response => {
          const data = await response.json()

          if (response.status === 401) {
            console.log(data)
          } else {
            console.log(data.access_token)

            VueCookies.set('access_token', data.access_token, 60 * 5)
            VueCookies.set('refresh_token', data.refresh_token, 60 * 10)
          }
        })
    }
  }
}
</script>

<style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand');
    .login {
        position: absolute;
        font-family: 'Quicksand', sans-serif;
        border: 1px solid #57bb55;
        border-radius: 25px;
        width: 40%;
        height: 700px;
    }
</style>
