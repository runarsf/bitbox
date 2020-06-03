<template>
  <div class='userSettings'>
    <input type='text' v-model='fullName' placeholder='Full Name'><br />
    <button @click='updateProfile'>Submit</button>
  </div>
</template>

<script>
//import firebase from 'firebase';

export default {
  name: 'userSettings',
  data () {
    return {
      fullName: ''
    }
  },
  methods: {
    updateProfile: function () {
      /*let changeRequest = Auth.auth().currentUser?.createProfileChangeRequest()
      changeRequest?.displayName = this.fullName
      changeRequest?.commitChanges { (error) in
        return 'ok'
      }*/
    }
  }
}
</script>
