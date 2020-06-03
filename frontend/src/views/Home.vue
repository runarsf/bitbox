<template>
  <div class='home'>
    <HelloWorld msg='Welcome!' />
    <p>{{ email }} :: {{ uid }}</p>
    <button @click='logout'>Logout</button>
    <button @click='userSettings'>Edit Profile</button>
    <button @click='images'>Images</button>
  </div>
</template>

<script>
import firebase from 'firebase';
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {
    HelloWorld
  },
  data: function () {
    return {
      email: null,
      uid: null
    }
  },
  created: function () {
    let user = firebase.auth().currentUser;
    this.email = user.email;
    this.uid = user.uid;
  },
  methods: {
    logout: function () {
      firebase.auth().signOut().then(() => {
        this.$router.replace('login');
      })
    },
    images: function () {
      this.$router.replace('images');
    },
    userSettings: function () {
      this.$router.replace('userSettings');
    }
  }
}
</script>
