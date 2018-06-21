function unlike(pos, id) {
  $.ajax({
    url: '/api/v1/likes/' + id,
    type: 'DELETE',
    dataType: 'json',
    data: {'id': id},
    statusCode: {
      204: function() {
        $("#playlist li").each( function (i) {
          if(i == pos) {
            $(this).remove();
          }
        });
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
    'url': '/api/v1/likes/usuario/' + usuario_id,
    'type': 'GET',
    success: function (data) {
      musicas = data;
      for(var i = 0; i < data.length; i++) {
          playlist.push({
            'src': musicas[i].musica.arquivo,
            'desc': musicas[i].musica.nome
          });
          if(musicas[i].musica.duracao)
          {
            $("#playlist").append("<li class='list-group-item' data-id='"+ musicas[i].musica.id +"' data-pos='"+ i +"'><div class='like liked' onClick=unlike("+ i +","+ musicas[i].id +")><i class='fas fa-heart'></i></div><div onClick='changeSong(" + i + ")' class='music-info'>"+ musicas[i].musica.nome + " <span class='badge badge-warning'>" + musicas[i].musica.duracao.substr(3, 5) + "</div></li>");
          } else {
            $("#playlist").append("<li class='list-group-item' data-id='"+ musicas[i].musica.id +"' data-pos='"+ i +"'><div onClick='changeSong(" + i + ")' class='music-info'><div class='like liked' onClick=unlike("+ i +","+ musicas[i].id +")><i class='fas fa-heart'></i></div>"+ musicas[i].musica.nome + " <span class='badge badge-warning'>" + '00:00' + "</div></li>");
          }
      }
    }
  });
});
