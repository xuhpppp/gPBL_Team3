<template>
    <NewOrder @inputData="updateNewOrder"></NewOrder>
    <OrderList :orderList="order_list" :orderListUser="order_list_user" :isHost="is_host" @inputData="filterOrder"></OrderList>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'
import NewOrder from '@/components/NewOrder.vue'
import OrderList from '@/components/OrderList.vue'

export default {
  components: {
    NewOrder,
    OrderList
  },
  data () {
    return {
      order_list: [],
      order_list_user: [],
      is_host: []
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

    const getMyOrders = {
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
      fetch('http://127.0.0.1:8000/room/order-list', getMyOrders)
        .then(async response => {
          const data = await response.json()

          if (response.status === 200) {
            this.order_list = data.order_list
            this.order_list_user = data.order_list_user
            this.is_host = data.is_host

            this.order_list = this.order_list.reverse()
            this.order_list_user = this.order_list_user.reverse()
            this.is_host = this.is_host.reverse()
          } else {
            router.push('/login')
          }
        })
    }
  },
  methods: {
    updateNewOrder (neworder) {
      this.order_list.unshift(neworder)
      this.order_list_user.unshift(neworder.user)
      this.is_host.unshift(1)
    },
    filterOrder (neworderlist) {
      this.order_list = neworderlist.filtered_order_list.reverse()
      this.order_list_user = neworderlist.filtered_order_list_user.reverse()
      this.is_host = neworderlist.filtered_is_host.reverse()
    }
  }
}
</script>
