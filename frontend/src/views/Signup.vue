<template>
  <div class='signup'>
    <h3>New Account</h3>
    <input type='text' v-model='email' placeholder='Email'><br />
    <input type='password' v-model='password' placeholder='Password'><br />
    <button @click='signup'>Sign Up</button>
    <p>Already have an account? <router-link to='/login'>Sign in!</router-link></p>
  </div>
</template>

<script>
import firebase from 'firebase';

export default {
  name: 'signup',
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    signup: function () {
      firebase.auth().createUserWithEmailAndPassword(this.email, this.password).then(
        (user) => {
          // https://stackoverflow.com/questions/40389946/how-do-i-set-the-displayname-of-firebase-user/40429080
          this.$router.replace('home');
          user;
        },
        (err) => {
          // https://firebase.google.com/docs/reference/js/firebase.auth.Auth.html#createuserwithemailandpassword
          // https://www.youtube.com/watch?v=7b2l3hB2oZc
          alert(err.message);
        }
      );
    }
  }
}
</script>

<style scoped>
/*.signup {
  margin-top: 40px;
}
input {
  margin: 10px 0;
  width: 20%;
  padding: 15px;
}
button {
  margin-top: 20px;
  width: 10%;
  cursor: pointer;
}
p {
  margin-top: 40px;
  font-size: 13px;
}
p a {
  text-decoration: underline;
  cursor: pointer;
}*/
</style>