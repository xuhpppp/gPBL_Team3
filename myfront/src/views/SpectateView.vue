<template>
  <h1>hello</h1>
</template>

<script>
export default {
  created () {
    const socket = new WebSocket('ws://localhost:8000/ws/count')

    console.log(socket)
  }
}
</script>
