<template>
    <div class="list">
        <h1 class="list-title">Order list</h1>

        <p class="list-note"><i>If something isn't displayed right, please refresh</i></p>

        <div class="list-edit">
          <label class="list-edit-label">From:</label>
          <input class="list-edit-time" type="datetime-local" v-model="from"/>

          <label class="list-edit-label">To:</label>
          <input class="list-edit-time" type="datetime-local" v-model="to"/>

          <font-awesome-icon class="list-edit-icon" icon="fa-solid fa-rotate" @click="filter_time"/>
        </div>

        <table class="list-table">
            <tr class="list-table-row">
                <th class="list-table-row-header">Room name</th>
                <th class="list-table-row-header">Start time</th>
                <th class="list-table-row-header">End time</th>
                <th class="list-table-row-header">Host</th>
                <th class="list-table-row-header"></th>
            </tr>

            <tr class="list-table-row" v-for="(order, index) in orderList" :key="order">
                <th class="list-table-row-header">{{ order.room_name }}</th>
                <th class="list-table-row-header">{{ order.start_time.slice(0, 16).replace('T', ' ') }}</th>
                <th class="list-table-row-header">{{ order.end_time.slice(0, 16).replace('T', ' ') }}</th>
                <th class="list-table-row-header">{{ orderListUser[index] }}</th>
                <th class="list-table-row-header">
                  <a :href="'/edit-order/' + order.id" class="list-table-row-header" v-if="isHost[index]==1">Edit</a>
                  <p class="list-table-row-header" style="color: gray; margin: 0" v-else>Edit</p>
                </th>
            </tr>
        </table>
    </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'

export default {
  props: {
    orderList: Array,
    orderListUser: Array,
    isHost: Array
  },
  data () {
    return {
      filtered: {
        filtered_order_list: [],
        filtered_order_list_user: [],
        filtered_is_host: []
      },
      from: '',
      to: ''
    }
  },
  methods: {
    filter_time () {
      if (this.from === '' && this.to === '') {
        location.reload()

        return
      }

      const filterOrder = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + VueCookies.get('access_token')
        },
        body: JSON.stringify({
          start_time: this.from.replaceAll('T', ' '),
          end_time: this.to.replaceAll('T', ' ')
        })
      }

      fetch('http://127.0.0.1:8000/room/order-list', filterOrder)
        .then(async response => {
          const data = await response.json()

          if (response.status === 401) {
            router.push('/login')
          } else {
            if (response.status === 200) {
              // emit to update real-time
              this.filtered.filtered_order_list = data.filter_order
              this.filtered.filtered_order_list_user = data.order_list_user
              this.filtered.filtered_is_host = data.is_host

              this.$emit('inputData', this.filtered)
            }
          }
        })
    }
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  .list {
    font-family: 'Quicksand', sans-serif;
  }

  .list-title {
    text-align: center;
  }

  .list-note {
    text-align: center;
  }

  .list-table {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 20px;
    font-size: 22px;
  }

  td, th {
    border: 1px solid #57bb55;
    padding-left: 10px;
    padding-right: 10px;
  }

  .list-edit {
    text-align: center;
  }

  .list-edit-label {
    font-size: 22px;
    font-weight: 600;
    margin-right: 10px;
  }

  .list-edit-time {
    height: 30px;
    width: 220px;
    border: 1px solid green;
    border-radius: 24px;
    padding-left: 20px;
    padding-right: 10px;
    margin-right: 30px;
  }

  .list-edit-icon {
    cursor: pointer;
    font-size: 26px;
  }

  .list-edit-icon:hover {
    color: #57bb55;
    transition: 0.3s;
    transform: rotate(360deg);
  }
</style>
