<template>
    <div class="list">
        <h1 class="list-title">Order list</h1>

        <div class="list-edit">
           <h1>a</h1>
        </div>

        <table class="list-table">
            <tr class="list-table-row">
                <th class="list-table-row-header">Room name</th>
                <th class="list-table-row-header">Start time</th>
                <th class="list-table-row-header">End time</th>
                <th class="list-table-row-header">Host</th>
            </tr>

            <tr class="list-table-row" v-for="(order, index) in orderList" :key="order">
                <th class="list-table-row-header">{{ order.room_name }}</th>
                <th class="list-table-row-header">{{ order.start_time.slice(0, 16).replace('T', ' ') }}</th>
                <th class="list-table-row-header">{{ order.end_time.slice(0, 16).replace('T', ' ') }}</th>
                <th class="list-table-row-header">{{ orderListUser[index] }}</th>
            </tr>
        </table>
    </div>
</template>

<script>
export default {
  props: {
    orderList: Array,
    orderListUser: Array
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
</style>
