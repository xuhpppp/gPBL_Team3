<template>
    <div class="room">
        <div class="room-info" v-for="(name, index) in room_name" :key="name" :class="{ available: 1-roomCondition[index] }">
            <font-awesome-icon class="room-info-icon" icon="fa-solid fa-computer" />
            <h1 class="room-info-name">Room {{name}}</h1>
            <p class="room-info-condition" v-if="roomCondition[index] == 0">Available to order</p>
            <p class="room-info-condition" v-else>Being in use</p>
        </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      room_name: ['101', '201', '301']
    }
  },
  props: {
    roomCondition: Array
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  .available {
    color: green;
  }

  .room {
    position: absolute;
    font-family: 'Quicksand', sans-serif;
    background-color: white;
    border-radius: 24px;
    margin-top: 280px;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    color: red;
  }

  .room-info {
    text-align: center;
    padding-top: 30px;
  }

  .room-info-icon {
    font-size: 90px;
  }

  .room-info-condition {
    font-size: 20px;
  }

  @media (max-width: 1280px) {
    .room {
      width: 100%;
    }
  }
</style>
