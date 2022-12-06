<template>
    <div class="select">
        <div class="select-element">101</div>

        <div class="select-element">201</div>

        <div class="select-element">301</div>
    </div>

    <div class="stream">
        <!-- http://127.0.0.1:8000/video_feed/ -->
        <img :src="main_link" alt="">
    </div>

    <div class="info">
        <!-- dev here... -->
    </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  data () {
    return {
      link_101: '',
      link_201: '',
      link_301: '',
      main_link: ''
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

    const checkAdmin = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + VueCookies.get('access_token')
      }
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
    } else {
      fetch('http://127.0.0.1:8000/authen/admin', checkAdmin)
        .then(async response => {
          const data = await response.json()

          if (response.status === 401) {
            router.push('/')
          } else {
            this.main_link = data.link_101
            this.link_101 = data.link_101
          }
        })
    }
  }
}
</script>
