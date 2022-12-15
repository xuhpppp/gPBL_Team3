<template>
  <div class="row">
    <div class="col-sm-12 col-xl-4 mt-4">
      <div class="bg-light rounded h-100 p-4">
        <h6 class="mb-4">Face </h6>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Time</th>
              <th scope="col">Image</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in face_pass" v-bind:key="index">
              <th scope="row">{{ index }}</th>
              <td>{{ item.name }}</td>
              <td>{{ item.time }}</td>
              <td><img :src="api_url + '/image/' + item.path" alt=""></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="col-sm-12 col-xl-4 mt-4">
      <div class="bg-light rounded h-100 p-4">
        <h6 class="mb-4">Not registered in the room</h6>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Time</th>
              <th scope="col">Image</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in face_not_shift" v-bind:key="index">
              <th scope="row">{{ index }}</th>
              <td>{{ item.name }}</td>
              <td>{{ item.time }}</td>
              <td><img :src="api_url + '/image/' + item.path" alt=""></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="col-sm-12 col-xl-4 mt-4">
      <div class="bg-light rounded h-100 p-4">
        <h6 class="mb-4">Unrecognizable</h6>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Time</th>
              <th scope="col">Image</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in face_unknow" v-bind:key="index">
              <th scope="row">{{ index }}</th>
              <td>{{ item.name }}</td>
              <td>{{ item.time }}</td>
              <td><img :src="api_url + '/image/' + item.path" alt=""></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script>
import commons from '@/commons'
import VueCookies from 'vue-cookies'

export default {
  data() {
    return {
      face_pass: [],
      face_not_shift: [],
      face_unknow: [],
      api_url: commons.API_URL
    }
  },

  mounted() {
    const getRecogData = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + VueCookies.get('access_token')
      }
    }

    setInterval(() => {
      fetch(commons.API_URL + '/recog/', getRecogData)
        .then(async response => {
          const data = await response.json()
          console.log(data)
          if (response.status === 200) {
            this.face_pass = data.list_success
            this.face_not_shift = data.list_not_success
            this.face_unknow = data.list_unknow
          }
        })
    }, 1000)
  }
}

</script>


