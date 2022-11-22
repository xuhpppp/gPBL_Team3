<template>
    <div class="option">
        <button class="option-button">
            <font-awesome-icon icon="fa-solid fa-calendar-days option-button-icon" />
            <p class="option-button-text">My order</p>
        </button>

        <button class="option-button" v-if="isAdmin == true">
            <font-awesome-icon icon="fa-solid fa-list-check option-button-icon" />
            <p class="option-button-text">Order management</p>
        </button>

        <button class="option-button" v-if="isAdmin == true">
            <font-awesome-icon icon="fa-solid fa-video option-button-icon" />
            <p class="option-button-text">Spectate rooms</p>
        </button>

        <button class="option-button" v-if="isAdmin == true">
            <font-awesome-icon icon="fa-solid fa-user-plus option-button-icon" />
            <p class="option-button-text">Register new user</p>
        </button>

        <button class="option-button">
            <font-awesome-icon icon="fa-solid fa-key option-button-icon" />
            <p class="option-button-text">Change password</p>
        </button>

        <button class="option-button" @click="logout">
            <font-awesome-icon icon="fa-solid fa-power-off option-button-icon" />
            <p class="option-button-text">Log out</p>
        </button>
    </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  props: {
    isAdmin: Boolean
  },
  methods: {
    logout () {
      const userLogout = {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + VueCookies.get('access_token')
        }
      }

      fetch('http://127.0.0.1:8000/authen/logout', userLogout)
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
    width: 1000px;
    left: 50%;
    transform: translateX(-50%);
    background-color: rebeccapurple;
  }
</style>
