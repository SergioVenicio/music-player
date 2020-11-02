function unlike(el) {
  let id = $(el).parent().attr('like-id');
  $.ajax({
    url: '/api/v1/likes/' + id,
    type: 'DELETE',
    statusCode: {
      204: function() {
          var el_pos = parseInt($(el).parent().children('.music-info').children('.ordem').text());
          playlist.pop($(el).parent().attr('data-pos'));
          $("#playlist li").each( function () {
            if($(this).children('.music-info').children('.ordem').text() >= el_pos){
              var ordem = parseInt($(this).children('.music-info').children('.ordem').text());
              $(this).children('.music-info').children('.ordem').text(ordem - 1);
            }
          });
          $(el).parent().remove();
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
    url: '/api/v1/likes',
    type: 'GET',
    data: {
      user_id: usuario_id
    },
    success: function (data) {
      musicas = data.map(({music}) => music);
      console.log(musicas)
      for(var i = 0; i < data.length; i++) {
          playlist.push({
            'src': musicas[i].file,
            'desc': musicas[i].name
          });
          if(musicas[i].duration)
          {
            $("#playlist").append("<li class='list-group-item' data-id='" + musicas[i].id + "' data-pos='" + i + "' like-id='" + data[i].id + "'><div class='like liked' onClick=unlike(this)><i class='fas fa-heart'></i></div><div onClick='changeSong(" + i + ")' class='music-info'><div class='ordem'>" + (i + 1) + "</div> - " + musicas[i].name + " <span class='badge badge-warning'>" + musicas[i].duration.substr(3, 5) + "</div></li>");
          } else {
            $("#playlist").append("<li class='list-group-item' data-id='" + musicas[i].id +"' data-pos='"+ i +"' like-id='" + data[i].id + "'><div onClick='changeSong(" + i + ")' class='music-info'><div class='like liked' onClick=unlike("+ i +","+ musicas[i].id +")><i class='fas fa-heart'></i></div><div class='ordem'>" + (i + 1) + "</div> - " + musicas[i].name + " <span class='badge badge-warning'>" + '00:00' + "</div></li>");
          }
      }
    }
  });
});
