$(document).ready(function() {
  let options = {
    'autoplay': false
  }
  let controls = `
  <div class="plyr__controls">
      <button type="button" class="plyr__control" data-plyr="restart">
          <svg role="presentation"><use xlink:href="#plyr-restart"></use></svg>
          <span class="plyr__tooltip" role="tooltip">Restart</span>
      </button>
      <button type="button" class="plyr__control" data-plyr="rewind">
          <svg role="presentation"><use xlink:href="#plyr-rewind"></use></svg>
          <span class="plyr__tooltip" role="tooltip">Rewind {seektime} secs</span>
      </button>
      <button type="button" class="plyr__control" aria-pressed="false" aria-label="Play, {title}" data-plyr="play">
          <svg class="icon--pressed" role="presentation"><use xlink:href="#plyr-pause"></use></svg>
          <svg class="icon--not-pressed" role="presentation"><use xlink:href="#plyr-play"></use></svg>
          <span class="label--pressed plyr__tooltip" role="tooltip">Pause</span>
          <span class="label--not-pressed plyr__tooltip" role="tooltip">Play</span>
      </button>
      <button type="button" class="plyr__control" data-plyr="fast-forward">
          <svg role="presentation"><use xlink:href="#plyr-fast-forward"></use></svg>
          <span class="plyr__tooltip" role="tooltip">Forward {seektime} secs</span>
      </button>
      <div class="plyr__progress">
          <label for="plyr-seek-{id}" class="plyr__sr-only">Seek</label>
          <input data-plyr="seek" type="range" min="0" max="100" step="0.01" value="0" id="plyr-seek-{id}">
          <progress class="plyr__progress--buffer" min="0" max="100" value="0">% buffered</progress>
          <span role="tooltip" class="plyr__tooltip">00:00</span>
      </div>
      <div class="plyr__time plyr__time--current" aria-label="Current time">00:00</div>
      <div class="plyr__time plyr__time--duration" aria-label="Duration">00:00</div>
      <button type="button" class="plyr__control" aria-pressed="false" aria-label="Mute" data-plyr="mute">
          <svg class="icon--pressed" role="presentation"><use xlink:href="#plyr-muted"></use></svg>
          <svg class="icon--not-pressed" role="presentation"><use xlink:href="#plyr-volume"></use></svg>
          <span class="label--pressed plyr__tooltip" role="tooltip">Unmute</span>
          <span class="label--not-pressed plyr__tooltip" role="tooltip">Mute</span>
      </button>
      <div class="plyr__volume">
          <label for="plyr-volume-{id}" class="plyr__sr-only">Volume</label>
          <input data-plyr="volume" type="range" min="0" max="1" step="0.05" value="1" autocomplete="off" id="plyr-volume-{id}">
      </div>
      <button type="button" class="plyr__control" aria-pressed="true" aria-label="Enable captions" data-plyr="captions">
          <svg class="icon--pressed" role="presentation"><use xlink:href="#plyr-captions-on"></use></svg>
          <svg class="icon--not-pressed" role="presentation"><use xlink:href="#plyr-captions-off"></use></svg>
          <span class="label--pressed plyr__tooltip" role="tooltip">Disable captions</span>
          <span class="label--not-pressed plyr__tooltip" role="tooltip">Enable captions</span>
      </button>
      <button type="button" class="plyr__control" aria-pressed="false" aria-label="Enter fullscreen" data-plyr="fullscreen">
          <svg class="icon--pressed" role="presentation"><use xlink:href="#plyr-exit-fullscreen"></use></svg>
          <svg class="icon--not-pressed" role="presentation"><use xlink:href="#plyr-enter-fullscreen"></use></svg>
          <span class="label--pressed plyr__tooltip" role="tooltip">Exit fullscreen</span>
          <span class="label--not-pressed plyr__tooltip" role="tooltip">Enter fullscreen</span>
      </button>
  </div>
  `;
  let player = new Plyr('#player', {controls});
  let musicas = [];
  $.ajax({
    'url': '/api_v1/musicas/album/' + album_id,
    'type': 'GET',
    success: function (data) {       
      for(var i = 0; i < data.length; i++) {
          musicas.push({
            'src': data[i].arquivo,
            'type': 'audio/mp3'
          });
          $("#playlist").append("<li class='list-group-item'>" + data[i].nome + "</li>");
      }
      player.source = {
        type: 'audio',
        title: 'Music Player',
        sources: musicas
      }
    }
  });
})