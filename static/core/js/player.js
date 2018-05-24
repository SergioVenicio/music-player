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
        }
      }
    });
    $(".pause").hide();
    _player.volume = 0.3;
    _player.controls = true;


  function player(x) {
    var i = 0;
    _player.src = playlist[x]; // x is the index number of the playlist array
    _player.load();            // use the load method when changing src
    _player.play();
    _player.onended = function() { // Once the initial file is played it plays the rest of the files
      i++;
      if (i > playlist.length) {
        i = 0;
      }
      _player.src = playlist[i];
      if(time != 0) {
          _player.play();
      } else {
          _player.load();            // Lather, ^
          _player.play();              // and.....^
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
