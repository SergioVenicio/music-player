$(document).ready(function() {
  let options = {
    'autoplay': false
  }
  let player = new Plyr('#player');
  let musicas = [];
  $.ajax({
    'url': '/api_v1/musicas/album/' + album_id,
    'type': 'GET',
    success: function (data) {       
      for(var i = 0; i < data.length; i++) {
          musicas.push({
            'src': data[i].arquivo,
            'type': 'audio/mp3'
          });
          $("#playlist").append("<li class='list-group-item'>" + data[i].nome + "</li>");
      }
      player.source = {
        type: 'audio',
        title: 'Music Player',
        sources: musicas
      }
    }
  });
})