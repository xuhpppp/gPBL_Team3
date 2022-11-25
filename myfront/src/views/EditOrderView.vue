<template>
  <EditOrder></EditOrder>
    <div class="staff">
      <h1 class="staff-title">List of staffs</h1>

      <div class="staff-add">
        <label class="staff-add-lable">Add a guess:</label>
        <input class="staff-add-input" type="email" placeholder="Staff email...">
        <button class="staff-add-button">Add</button>
      </div>
    </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'
import EditOrder from '../components/EditOrder.vue'

export default {
  components: {
    EditOrder
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
  }
}
</script>

<style scoped>
  .staff {
    font-family: 'Quicksand', sans-serif;
    position: relative;
    text-align: center;
  }
</style>
