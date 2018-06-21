function like(pos, usuario_id, musica_id) {
  $.ajax({
    url: '/api/v1/likes',
    type: 'POST',
    dataType: 'json',
    data: {'usuario': usuario_id, 'musica': musica_id},
    statusCode: {
      201: function(data) {
        data = JSON.parse(data);
        if(data.like) {
          $("#playlist li").each( function (i) {
            if(i == pos) {
              $(this).children('.like').addClass('liked');
            }
          });
        } else {
          $("#like_modal").modal();
        }
      },
      400: function(data) {
        data = JSON.parse(data.responseJSON);
        $("#like_modal").modal();
      }
    }
  });
}

$(document).ready( function (){
  $.ajax({
    'url': '/api/v1/musicas/album/' + album_id,
    'type': 'GET',
    success: function (data) {
      response_musicas = data;
      for(var i = 0; i < data.length; i++) {
          playlist.push({
            'src': response_musicas[i].arquivo,
            'desc': response_musicas[i].nome
          });
          if(response_musicas[i].duracao)
          {
            $("#playlist").append("<li class='list-group-item' data-id='"+ response_musicas[i].id +"' data-pos='"+ i +"'><div class='like' onClick=like("+ i +","+ usuario_id +","+ response_musicas[i].id +")><i class='fas fa-heart'></i></div><div onClick='changeSong(" + i + ")' class='music-info'>"+ response_musicas[i].nome + " <span class='badge badge-warning'>" + response_musicas[i].duracao.substr(3, 5) + "</div></li>");
          } else {
            $("#playlist").append("<li class='list-group-item' data-id='"+ response_musicas[i].id +"' data-pos='"+ i +"'><div class='like' onClick=like("+ i +","+ usuario_id, response_musicas[i].id +")><i class='fas fa-heart'></i></div><div onClick='changeSong(" + i + ")' class='music-info'>"+ response_musicas[i].nome + " <span class='badge badge-warning'>" + '00:00' + "</div></li>");
          }

          var _musicas = $("#playlist li");

          $.ajax({
            'url': '/api/v1/likes/usuario/' + usuario_id + '/' + data[i].id,
            'type': 'GET',
            success: function (data) {
              if(data.length > 0) {
                for(let m = 0; m < _musicas.length; m++) {
                  if($(_musicas[m]).attr('data-id') == data[0].musica) {
                    $(_musicas[m]).children('.like').addClass('liked');
                  }
                }
              }
            }
          });
      }
    }
  });
});
