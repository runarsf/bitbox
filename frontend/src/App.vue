<template>
  <div id='app'>
    <!-- <img alt='Vue logo' src='./assets/logo.png'> -->
    <object data='/bitbox.svg' type='image/svg+xml' width='200rem' height='200rem'>
      <img src='/bitbox.png' style='width: 200rem; height: 200rem;' />
    </object>
    <!--<div id='nav'>
      <router-link to='/home'>Home</router-link> |
      <router-link to='/login'>Login</router-link> |
      <router-link to='/signup'>Sign Up</router-link>
    </div>-->
    <router-view class='router-view' />
  </div>
</template>

<style>
/** {
  padding: 0;
  margin: 0;
}
html,
body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  width: 100%;
  height: 100%;
}
.router-view {
  position: absolute;
  margin: auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 30%;
  height: 45%;
  border-radius: 3px;

  -webkit-box-shadow: 0px 0px 5px 1px rgba(0,0,0,0.59);
  -moz-box-shadow: 0px 0px 5px 1px rgba(0,0,0,0.59);
  box-shadow: 0px 0px 5px 1px rgba(0,0,0,0.59);
}
.router-view button {
}*/
/*
#nav {
  padding: 30px;
}
#nav a {
  font-weight: bold;
  color: #2c3e50;
}
#nav a.router-link-exact-active {
  color: #42b983;
}*/
</style>
