<template>
  <div class='login'>
    <h1>Sign In</h1>
    <input type='text' v-model='email' placeholder='Email'><br />
    <input type='password' v-model='password' placeholder='Password'><br />
    <!--<p>Forgot password</p>-->
    <button @click='login'>Sign In</button>
    <p>Don't have an account? <router-link to='/signup'>Sign up</router-link></p>
  </div>
</template>

<script>
import firebase from 'firebase';

export default {
  name: 'login',
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    login: function () {
      firebase.auth().signInWithEmailAndPassword(this.email, this.password).then(
        (user) => {
          this.$router.replace('home');
          user;
        },
        (err) => {
          alert(err.message);
        }
      )
    }
  }
}
</script>

<style scoped>
/*.login {
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