var mus = 0;
var volume = 1;
var _player = document.getElementById("audio");
var playlist = [];
var musica_ativa = '';
var musicas_tocadas = [];
var end_playlist = false;
var repeat = false;
var random = false;


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

function get_random_music(random_int) {
  if(musicas_tocadas.length < playlist.length) {
    if(!musicas_tocadas.includes(random_int)) {
      musicas_tocadas.push(random_int);
      changeSong(random_int);
    } else {
      var random_music = Math.floor(Math.random() * playlist.length);
      get_random_music(random_music);
    }
  } else {
    player(playlist.length+1);
  }
}

function player(music=0) {
  var musicas = $("#playlist li");
  if(music < 0) {
    mus = 0;
    music = 0;
  }
  if(music < playlist.length) {
    $(musica_ativa).removeClass('music-active');
    if(!$(musica_ativa).children('.like').hasClass('liked')) {
      $(musica_ativa).children('.like').css('color', '#919aa1');
    }
    for(i = 0; i <= musicas.length; i++) {
      if($(musicas[i]).attr('data-pos') == music) {
        musica_ativa = $(musicas[i]);
        $(musica_ativa).addClass('music-active');
        if(!$(musicas[i]).children('.like').hasClass('liked')) {
          $(musica_ativa).children('.like').css('color', '#F5F5F5');
        }
      }
    }
    $(".music-description").text(playlist[music].desc);
    _player.src = playlist[music].src;
    _player.load();
    _player.play();
    _player.loaded = true;
    $(".pause").show();
    $(".play").hide();
  } else {
    if(repeat) {
        mus = 0;
        music = 0;
        musicas_tocadas = [];
        player();
    } else {
      $(".music-description").text('A playlist acabou');
    }
  }
}

function changeSong(music) {
  mus = music;
  player(mus);
}

$(document).ready(function() {
    $(".mute").hide();
    var player = '';

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

    $(".pause").hide();

    _player.volume = 1;
    $("#vol-control").val(100);
    _player.controls = true;

  $("#vol-control").on({
      change: function () {
          _player.volume = $(this).val() / 100;
      }
  });

  $(".volume").on({
    click: function () {
      $(this).hide()
      $(".mute").show();
      _player.volume = 0;
    }
  });

  $(".mute").on({
    click: function () {
      $(this).hide()
      $(".volume").show();
      _player.volume = volume;
    }
  });

  $(".pause-play").on({
      click: function () {
          if(!_player.paused) {
            $(".pause").hide();
            $(".play").show();
            _player.pause();
        } else {
          $(".pause").show();
          $(".play").hide();
          if(_player.loaded) {
              _player.play();
          } else {
            if(!random) {
              changeSong(mus);
            } else {
              get_random_music(Math.floor(Math.random() * playlist.length));
            }
          }
        }
      }
  });

  $(".repeat").on({
    click: function () {
      if($(this).hasClass('control-active')) {
        $(this).removeClass('control-active');
        repeat = false;
      } else {
        $(this).addClass('control-active');
        repeat = true;
      }
    }
  });

  $(".random").on({
    click: function () {
      if($(this).hasClass('control-active')) {
        $(this).removeClass('control-active');
        random = false;
      } else {
        $(this).addClass('control-active');
        random = true;
      }
    }
  });

  $(".next").on({
    click: function() {
      if(!random) {
        mus = mus + 1;
        changeSong(mus);
      } else {
        get_random_music(Math.floor(Math.random() * playlist.length));
      }
    }
  })

  $(".prev").on({
    click: function () {
      if(!random) {
        mus = mus - 1;
        changeSong(mus);
      } else {
        get_random_music(Math.floor(Math.random() * playlist.length));
      }
    }
  });

  $("#audio").on({
    'ended': function () {
      if(!random) {
        mus = mus + 1;
        changeSong(mus);
      } else {
        get_random_music(Math.floor(Math.random() * playlist.length));
      }
    }
  });

  $("#vol-control").on({
    'change': function () {
      volume = $(this).val();
      volume = volume / 100;
      _player.volume = volume;
      if($(this).val() == 0) {
        $(".volume").hide();
        $(".mute").show();
      } else {
        $(".mute").hide();
        $(".volume").show();
      }
    }
  });
});
