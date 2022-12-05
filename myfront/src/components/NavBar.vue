<template>
    <div class="navbar">
      <font-awesome-icon icon="fa-solid fa-address-card" class="navbar-icon" />

      <div class="navbar-text">
        <h1 class="navbar-text-welcome">Welcome</h1>

        <h1 class="navbar-text-fullname">{{ fullName }}</h1>
      </div>
    </div>
</template>

<script>
export default {
  props: {
    fullName: String
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  .navbar {
    font-family: 'Quicksand', sans-serif;
    background-color: white;
    position: absolute;
    display: flex;
    width: 500px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 24px;
    height: 144px;
    margin-top: 40px;
  }

  .navbar-icon {
    font-size: 60px;
    position: absolute;
    top: 50%;
    left: 15%;
    transform: translate(-50%, -50%);
  }

  .navbar-text {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
  }

  .navbar-text-fullname {
    color: #57bb55;
  }
</style>
