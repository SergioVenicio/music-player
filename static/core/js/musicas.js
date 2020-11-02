function unlike(pos, id) {
  $.ajax({
    url: '/api/v1/likes/' + id,
    type: 'DELETE',
    statusCode: {
      204: function() {
        $("#playlist li").each( function (i) {
          if(i == pos) {
            $(this).children('.like').removeClass('liked');
            $(this).removeAttr('like-id');
            $(this).children('.like').attr('onclick', "like(" + $(this).attr('data-pos') + ", " + usuario_id + ", " + $(this).attr('data-id') + ")");
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

function like(pos, usuario_id, musica_id) {
  $.ajax({
    url: '/api/v1/likes',
    type: 'POST',
    dataType: 'json',
    data: {
      'user_id': usuario_id,
      'music_id': musica_id
    },
    statusCode: {
      201: function(data) {
        data = JSON.parse(data);
        if(data.like) {
          $("#playlist li").each( function (i) {
            if(i == pos) {
              $(this).children('.like').addClass('liked');
              $(this).attr('like-id', data.like.id);
              $(this).children('.like').attr('onclick', "unlike(" + $(this).attr('data-pos') + ", " + $(this).attr('like-id') + ")");
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
    'url': '/api/v1/likes',
    'type': 'GET',
    'params': {
      'user_id': usuario_id
    },
    success: function(data) {
      liked_songs = data.map(({music}) => music.id);
      console.log(liked_songs)
    }
  }).then(() => {
    $.ajax({
      url: '/api/v1/music',
      type: 'GET',
      data: {
        album_id
      },
      success: function (data) {
        response_musicas = data;
        for(var i = 0; i < data.length; i++) {
            playlist.push({
              'src': response_musicas[i].file,
              'desc': response_musicas[i].name
            });
            if(response_musicas[i].duration)
            {
              $("#playlist").append("<li class='list-group-item' data-id='"+ response_musicas[i].id +"' data-pos='"+ i +"'><div class='like' onClick=like("+ i +","+ usuario_id +","+ response_musicas[i].id +")><i class='fas fa-heart'></i></div><div onClick='changeSong(" + i + ")' class='music-info'>" + response_musicas[i].order + " - " + response_musicas[i].name + " <span class='badge badge-warning'>" + response_musicas[i].duration.substr(3, 5) + "</div></li>");
            } else {
              $("#playlist").append("<li class='list-group-item' data-id='"+ response_musicas[i].id +"' data-pos='"+ i +"'><div class='like' onClick=like("+ i +","+ usuario_id, response_musicas[i].id +")><i class='fas fa-heart'></i></div><div onClick='changeSong(" + i + ")' class='music-info'>"+ response_musicas[i].order + " - " + response_musicas[i].name + " <span class='badge badge-warning'>" + '00:00' + "</div></li>");
            }
  
            var _musicas = $("#playlist li");
            for(let m = 0; m < _musicas.length; m++) {
              if (liked_songs.includes(Number($(_musicas[m]).attr('data-id')))) {
                $(_musicas[m]).children('.like').addClass('liked');
                $(_musicas[m]).attr('like-id', liked_songs[0].id);
                $(_musicas[m]).children('.like').attr('onclick', "unlike(" + $(_musicas[m]).attr('data-pos') + ", " + data[0].id + ")");
              }
            }
        }
      }
    });
  });
});