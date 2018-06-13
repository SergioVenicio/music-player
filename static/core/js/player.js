var mus = 0;
var volume = 1;
var _player = document.getElementById("audio");
var playlist = [];
var musica_ativa = '';
var musicas_tocadas = [];
var end_playlist = false;
var repeat = false;
var random = false;


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
  var musicas = $("li");
  if(music < 0) {
    mus = 0;
    music = 0;
  }
  if(music < playlist.length) {
    $(musica_ativa).removeClass('music-active');
    for(i = 0; i <= musicas.length; i++) {
      if($(musicas[i]).attr('data-pos') == music) {
        musica_ativa = $(musicas[i]);
        $(musica_ativa).addClass('music-active');
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
        for(var i = 0; i < data.length; i++) {
            playlist.push({
              'src': data[i].arquivo,
              'desc': data[i].nome
            });
            if(data[i].duracao)
            {
              $("#playlist").append("<li onClick='changeSong(" + i + ")' class='list-group-item' data-pos='"+ i +"'>"+ data[i].nome + " <span class='badge badge-warning'>" + data[i].duracao.substr(3, 5) + "</li>");
            } else {
              $("#playlist").append("<li class='list-group-item' data-pos='" + i + "'>"+ data[i].nome + " <span class='badge badge-warning'>00:00</li>");
            }
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
