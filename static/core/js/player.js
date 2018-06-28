var _storage_album_id = localStorage.getItem("album_id");

if(localStorage.getItem("mus") && _storage_album_id == album_id) {
  var mus = parseInt(localStorage.getItem("mus"));
} else {
  var mus = 0;
  var _storage_album_id = localStorage.setItem("album_id", album_id);
}

if(localStorage.getItem("volume")) {
  var volume = localStorage.getItem("volume");
} else {
  var volume = 1;
}

if(localStorage.getItem("repeat") === "true") {
  var repeat = localStorage.getItem("repeat");
  $(".repeat").addClass('control-active');
} else {
  var repeat = false;
}

if(localStorage.getItem("random") === "true") {
  var random = localStorage.getItem("random");
  $(".random").addClass('control-active');
} else {
  var random = false;
}

localStorage.setItem("random", random);
localStorage.setItem("repeat", repeat);
localStorage.setItem("mus", mus);
localStorage.setItem("volume", volume);


var _player = document.getElementById("audio");
var playlist = [];
var musica_ativa = '';
var musicas_tocadas = [];
var end_playlist = false;


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
  localStorage.setItem("mus", mus);
}

$(document).ready(function() {
    $(".mute").hide();
    var player = '';

    $(".pause").hide();

    _player.volume = volume / 100;
    $("#vol-control").val(volume);
    _player.controls = true;

  $("#vol-control").on({
      change: function () {
          _player.volume = $(this).val() / 100;
          localStorage.setItem("volume", $(this).val());
      }
  });

  $(".volume").on({
    click: function () {
      $(this).hide()
      $(".mute").show();
      _player.volume = 0;
      localStorage.setItem("volume", 0);
    }
  });

  $(".mute").on({
    click: function () {
      $(this).hide()
      $(".volume").show();
      _player.volume = volume;
      localStorage.setItem("volume", volume);
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
      localStorage.setItem("repeat", repeat);
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
      localStorage.setItem("random", random);
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

$(document).keypress(function (e) {
  if(e.charCode === 32) {
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
  } else if (e.keyCode === 39) {
    if(!random) {
      mus++;
      changeSong(mus);
    } else {
      if(_player.paused) {
          _player.play();
      } else {
        get_random_music(Math.floor(Math.random() * playlist.length));
      }
    }
  } else if (e.keyCode === 37) {
    if(!random) {
      mus--;
      changeSong(mus);
    } else {
      get_random_music(Math.floor(Math.random() * playlist.length));
    }
  } else if (e.keyCode == 38) {
    if(_player.volume < 1) {
      var vol = parseInt($("#vol-control").val()) + 3;
      $("#vol-control").val(vol);
      _player.volume = (vol/ 100);
    }
  } else if (e.keyCode == 40) {
    if(_player.volume > 0) {
      var vol = parseInt($("#vol-control").val()) - 3;
      $("#vol-control").val(vol);
      _player.volume = vol / 100;
    }
  }
})
