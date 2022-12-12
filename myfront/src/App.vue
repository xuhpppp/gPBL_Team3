<template>
  <router-view/>
  <a class="home" href="/">
    <font-awesome-icon class="home-icon" icon="fa-solid fa-house" />
  </a>
</template>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Quicksand');

  body {
    background-color: #b8e3b8;
    margin: 0;
    padding: 0;
  }

  .home {
    position: fixed;
    right: 5%;
    bottom: 8%;
    border-radius: 100%;
    background-color: #57bb55;
    width: 50px;
    height: 50px;
  }

  .home-icon {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
  }
</style>
