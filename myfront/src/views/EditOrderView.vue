<template>
  <EditOrder></EditOrder>
  <AddStaff></AddStaff>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'
import EditOrder from '../components/EditOrder.vue'
import AddStaff from '../components/AddStaff.vue'
import commons from '@/commons'

export default {
  components: {
    EditOrder,
    AddStaff
  },
  created() {
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
        fetch(commons.API_URL + '/authen/refresh-token', refreshToken)
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
