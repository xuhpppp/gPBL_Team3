<template>
  <div class="option">
    <a class="option-button" href="/order">
      <font-awesome-icon class="option-button-icon" icon="fa-solid fa-calendar-days" />
      <p class="option-button-text">Order management</p>
    </a>

    <a class="option-button" v-if="isAdmin == true" href="/spectate">
      <font-awesome-icon class="option-button-icon" icon="fa-solid fa-video" />
      <p class="option-button-text">Spectate rooms</p>
    </a>

    <a class="option-button" v-if="isAdmin == true" href="/admin">
      <font-awesome-icon class="option-button-icon" icon="fa-solid fa-video" />
      <p class="option-button-text">Spectate rooms 2</p>
    </a>

    <a class="option-button" href="/face">
      <font-awesome-icon class="option-button-icon" icon="fa-solid fa-calendar-check" />
      <p class="option-button-text">Check-in</p>
    </a>

    <a class="option-button" href="/insert">
      <font-awesome-icon class="option-button-icon" icon="fa-solid fa-face-smile" />
      <p class="option-button-text">Insert dataset</p>
    </a>

    <a class="option-button" v-if="isAdmin == true">
      <font-awesome-icon class="option-button-icon" icon="fa-solid fa-user-plus" />
      <p class="option-button-text">Register new user</p>
    </a>

    <a class="option-button">
      <font-awesome-icon class="option-button-icon" icon="fa-solid fa-key" />
      <p class="option-button-text">Change password</p>
    </a>

    <a class="option-button" @click="logout">
      <font-awesome-icon class="option-button-icon" icon="fa-solid fa-power-off" />
      <p class="option-button-text">Log out</p>
    </a>
  </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'
import commons from '@/commons'

export default {
  props: {
    isAdmin: Boolean
  },
  methods: {
    logout() {
      const userLogout = {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + VueCookies.get('access_token')
        }
      }

      fetch(commons.API_URL + '/authen/logout', userLogout)
        .then(async response => {
          const data = await response.json()

          console.log(data.message)

          VueCookies.remove('access_token')
          VueCookies.remove('refresh_token')
          router.push('/login')
        })
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Quicksand');

.option {
  position: absolute;
  width: 80%;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Quicksand', sans-serif;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-top: 650px;
}

.option-button {
  width: 400px;
  height: 70px;
  border-radius: 34px;
  border: none;
  display: flex;
  align-items: center;
  padding-left: 80px;
  margin-bottom: 60px;
  cursor: pointer;
  background-color: white;
  text-decoration: none;
  color: black;
}

.option-button:hover {
  transition: 0.3s;
  background-color: #57bb55;
  color: white;
}

.option-button-icon {
  font-size: 34px;
}

.option-button-text {
  font-size: 20px;
  font-weight: 600;
  margin-left: 20px;
}
</style>
