<template lang="html">
  <div id="bands">
    <div class="mt-5"></div>
    <div class="container-fluid">
        <div class="container">
            <div class="row">
                <div v-for="(album, id) in albums" :key=id>
                  <div class="col-md-4">
                      <div class="card">
                        <img class="card-img-top" :src=album.capa>
                        <div class="card-body">
                          <h5 class="card-title">{{ album.nome }}</h5>
                          <p class="card-text"></p>
                          <div class="link-wrapper">
                            <a href="#" class="btn btn-warning">
                                Ouvir
                                <i data-feather="headphones"></i>
                            </a>
                          </div>
                        </div>
                      </div>
                  </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      albums: ''
    }
  },
  mounted () {
    axios.get('http://localhost:8000/api_v1/album/').then(
      response => (
        this.albums = response.data
      )
    ).catch(error => console.log(error))
  }
}
</script>

<style scoped>
#bg {
    display: none;
}
.card {
    width: 18rem;
}
.card > img {
    max-height: 13.5rem;
}
.link-wrapper {
  text-align: center;
}
</style>
