<template>
  <div class="login">
    <img class="login-img" src="../assets/admin.jpg" alt="">

    <div class="login-input">
      <h1 class="login-input-title">LOGIN</h1>
      <form action="" @submit.prevent="login_submit">
        <input class="login-input-email" type="text" placeholder="Type your email..." v-model="email">
        <input class="login-input-password" type="password" placeholder="Type your password..." v-model="password">

        <button type="submit" class="login-input-button" @click="login_submit">Login</button>
      </form>
      <p class="login-input-msg" v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'
import commons from '@/commons'

export default {
  data() {
    return {
      email: '',
      password: '',
      message: ''
    }
  },
  methods: {
    login_submit() {
      const LoginRequest = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.email,
          password: this.password
        })
      }

      fetch(commons.API_URL + '/authen/login', LoginRequest)
        .then(async response => {
          const data = await response.json()

          if (response.status === 401) {
            this.message = data.message
          } else if (response.status === 200) {
            VueCookies.set('access_token', data.access_token, 60 * 5)
            VueCookies.set('refresh_token', data.refresh_token, 60 * 10)

            router.push('/')
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
  border-radius: 25px;
  width: 74%;
  height: 700px;
  background-color: white;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  top: 50%;
}

.login-img {
  width: 30%;
  top: 50%;
  position: absolute;
  transform: translate(-50%, -50%);
  left: 20%;
}

.login-input {
  position: absolute;
  transform: translate(-50%, -50%);
  left: 64%;
  width: 30%;
  display: flex;
  flex-direction: column;
  top: 28%;
}

.login-input-title {
  font-size: 40px;
  left: 50%;
  position: absolute;
  transform: translateX(-50%);
}

.login-input-email {
  left: 50%;
  position: absolute;
  transform: translateX(-50%);
  margin-top: 100px;
  width: 74%;
  height: 34px;
  border-radius: 20px;
  border: 1px solid grey;
  padding-left: 20px;
  outline: none;
}

.login-input-email:hover {
  border: 1px solid #4caf45;
  transition: 0.3s;
}

.login-input-email:focus {
  border: 2px solid #0fdd00;
}

.login-input-password {
  left: 50%;
  position: absolute;
  transform: translateX(-50%);
  margin-top: 150px;
  width: 74%;
  height: 34px;
  border-radius: 20px;
  border: 1px solid grey;
  padding-left: 20px;
  outline: none;
}

.login-input-password:hover {
  border: 1px solid #4caf45;
  transition: 0.3s;
}

.login-input-password:focus {
  border: 2px solid #0fdd00;
}

.login-input-button {
  position: absolute;
  margin-top: 220px;
  width: 100px;
  height: 30px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 20px;
  border: 1px solid gray;
  background-color: transparent;
}

.login-input-button:hover {
  transition: 0.3s;
  border: 1px solid #4caf45;
  background-color: #4caf45;
  color: white;
  cursor: pointer;
}

.login-input-msg {
  color: red;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 300px;
  width: 100%;
  text-align: center;
}

@media (min-width: 741px) and (max-width: 1280px) {
  .login {
    width: 100%;
  }
}

@media (max-width: 740px) {
  .login {
    width: 100%;
    height: 100%;
    border-radius: 0px;
    background-color: transparent;
  }

  .login-input-title {
    color: white;
  }

  .login-img {
    display: none;
  }

  .login-input {
    left: 50%;
  }

  .login-input-email {
    width: 200%;
    background-color: transparent;
    border-color: white;
  }

  .login-input-email:focus {
    background-color: white;
  }

  .login-input-password {
    width: 200%;
    margin-top: 160px;
    background-color: transparent;
    border-color: white;
  }

  .login-input-password:focus {
    background-color: white;
  }

  .login-input-button {
    width: 200px;
    margin-top: 240px;
  }

  .login-input-button:hover {
    background-color: white;
    color: black;
  }
}
</style>
