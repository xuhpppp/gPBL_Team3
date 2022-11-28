<template>
    <div class="staff">
      <h1 class="staff-title">List of staffs</h1>

      <div class="staff-add">
        <label class="staff-add-label">Add a guess:</label>
        <input class="staff-add-input" type="email" placeholder="Staff email..." v-model="email">
        <button class="staff-add-button" @click="add_staff">Add</button>
      </div>

      <p class="staff-message">{{message}}</p>

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
      staff_list: [],
      staff_full_name: [],
      message: '',
      email: ''
    }
  },
  created () {
    const getStaffList = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + VueCookies.get('access_token')
      }
    }

    fetch('http://127.0.0.1:8000/room/staff-order/' + this.$route.params.idRoomOrder, getStaffList)
      .then(async response => {
        const data = await response.json()

        if (response.status === 200) {
          this.staff_list = data.staff_list
          this.staff_full_name = data.staff_full_name
        }
      })
  },
  methods: {
    add_staff () {
      const addStaff = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + VueCookies.get('access_token')
        },
        body: JSON.stringify({
          email: this.email
        })
      }

      fetch('http://127.0.0.1:8000/room/staff-order/' + this.$route.params.idRoomOrder, addStaff)
        .then(async response => {
          const data = await response.json()

          if (response.status === 404) {
            router.push('/order')
          } else if (response.status === 401) {
            router.push('/login')
          } else {
            this.message = data.message

            if (response.status === 200) {
              this.staff_list.push(data.staff_order)
              this.staff_full_name.push(data.full_name)
            }
          }
        })
    }
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');
  .staff {
    font-family: 'Quicksand', sans-serif;
    position: relative;
    text-align: center;
  }

  .staff-add-label {
    font-size: 20px;
  }

  .staff-add-input {
    width: 300px;
    height: 30px;
    border-radius: 26px;
    border: 1px solid #57bb55;
    outline: none;
    padding-left: 30px;
    margin-left: 10px;
    margin-right: 60px;
  }

  .staff-add-input:hover {
    transition: 0.3s;
    border: 2px solid green;
  }

  .staff-add-input:focus {
    border: 2px solid green;
  }

  .staff-add-button {
    width: 90px;
    height: 30px;
    border-radius: 24px;
    border: none;
    cursor: pointer;
  }

  .staff-add-button:hover {
    transition: 0.3s;
    background-color: green;
    color: white;
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
