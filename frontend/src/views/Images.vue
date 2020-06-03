<template>
  <div>
    <div id='images'></div>
    <button @click='logout'>Logout</button>
  </div>
</template>

<script>
import firebase from 'firebase';

/**
 * I trust using `firebase.auth().currentUser.email` as authentication because /images requires authentication.
 *  or user.uid
 */

export default {
  name: 'images',
  created: function () {
    this.loadImages();
  },
  methods: {
    logout: function () {
      firebase.auth().signOut().then(() => {
        this.$router.replace('login');
      })
    },
    loadImages: function () {
      console.log(firebase.auth().currentUser.uid);
    }
  }
}
</script>
