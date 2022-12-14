<template>
  <div class="spectate">
    <h2 class="spectate-log">{{ log }}</h2>

    <table class="staff-list">
        <tr class="staff-list-row">
          <th class="staff-list-row-header">Full name</th>
          <th class="staff-list-row-header">Joined</th>
        </tr>

        <tr class="staff-list-row" v-for="(staff, index) in staff_list" :key="staff">
          <th class="staff-list-row-header">{{ staff_full_name[index] }}</th>
          <th class="staff-list-row-header">
            <font-awesome-icon class="staff-list-row-header-icon" icon="fa-solid fa-check" v-if="staff.joined == true" />
            <font-awesome-icon class="staff-list-row-header-icon" icon="fa-solid fa-xmark" v-if="staff.joined == false" />
          </th>
        </tr>
      </table>
  </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  data () {
    return {
      log: 'Loading...',
      staff_list: [],
      staff_full_name: []
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
    } else {
      const getStaffList = {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + VueCookies.get('access_token')
        }
      }

      fetch('http://127.0.0.1:8000/room/staff-order/', getStaffList)
        .then(async response => {
          const data = await response.json()

          if (response.status === 200) {
            this.staff_list = data.staff_list
            this.staff_full_name = data.staff_full_name
          }
        })

      const socket = new WebSocket('ws://localhost:7000/ws/count')

      const self = this
      socket.onmessage = function (event) {
        var data = JSON.parse(event.data)

        self.log = data.log
      }
    }
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  .spectate {
    font-family: 'Quicksand', sans-serif;
    background-color: white;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    border-radius: 26px;
    margin-top: 60px;
    text-align: center;
    padding-top: 20px;
    height: 600px;
  }

  .staff-list {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 70px;
    font-size: 22px;
  }

  td, th {
    border: 1px solid #57bb55;
    padding-left: 10px;
    padding-right: 10px;
  }
</style>
