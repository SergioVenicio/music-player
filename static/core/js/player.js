var mus = 0;
var _player = document.getElementById("audio");

$(document).ready(function() {
    let playlist = [];
    $.ajax({
      'url': '/api_v1/musicas/album/' + album_id,
      'type': 'GET',
      success: function (data) {
        for(var i = 0; i < data.length; i++) {
            playlist.push(data[i].arquivo);
            if(data[i].duracao)
            {
              $("#playlist").append("<li class='list-group-item'>"+ data[i].nome + " <span class='badge badge-warning'>" + data[i].duracao.substr(3, 5) + "</li>");
            } else {
              $("#playlist").append("<li class='list-group-item'>"+ data[i].nome + " <span class='badge badge-warning'>00:00</li>");
            }
        }
      }
    });
    $(".pause").hide();
    _player.volume = 0.3;
    _player.controls = true;


  function player(x) {
    var i = 0;
    _player.src = playlist[x];
    _player.load();
    _player.play();
    _player.onended = function() {
      i++;
      if (i > playlist.length) {
        i = 0;
      }
      _player.src = playlist[i];
      if(time != 0) {
          _player.play();
      } else {
          _player.load();
          _player.play();
      }
    }
  }

  $("#vol-control").on({
      change: function () {
          _player.volume = $(this).val() / 100;
      }
  })

  $(".pause-play").on({
      click: function () {
          if(!_player.paused) {
             $(".pause").hide();
             $(".play").show();
            _player.pause();
        } else {
            $(".play").hide();
            $(".pause").show();
            player(mus);
        }
      }
  });

  $(".next").on({
    click: function() {
      mus = mus + 1;
      if(mus > playlist.length) {
        mus = 0;
      }
      player(mus);
    }
  })
  $(".prev").on({
    click: function () {
      mus = mus - 1;
      if(mus < 0) {
        mus = 0;
      }
      player(mus);
    }
  });
});
