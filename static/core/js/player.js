var mus = 0;
var volume = 1;
var _player = document.getElementById("audio");
var playlist = [];

function player(music=0) {
  if(music < 0) {
    music = 0;
  }
  if(music < playlist.length) {
    $(".music-description").text(playlist[music].desc);
    _player.src = playlist[music].src;
    _player.load();
    _player.play();
    _player.loaded = true;
    $(".pause").show();
    $(".play").hide();
  } else {
    $(".music-description").text('A playlist acabou');
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
      'url': '/api_v1/musicas/album/' + album_id,
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
            changeSong(mus);
          }
        }
      }
  });

  $(".next").on({
    click: function() {
      mus = mus + 1;
      changeSong(mus);
    }
  })
  $(".prev").on({
    click: function () {
      mus = mus - 1;
      changeSong(mus);
    }
  });

  $("#audio").on({
    'ended': function () {
      mus = mus + 1;
      changeSong(mus);
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
