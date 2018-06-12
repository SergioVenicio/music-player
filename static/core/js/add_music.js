$(document).ready( function (){
  $("#id_album").selectpicker();

  $("#id_arquivo").on({
    change: function () {
      let arquivo = document.getElementById('id_arquivo').files[0];
      let reader = new FileReader();
      reader.onload = function () {
        $("#file").val(reader.result);
      }
      reader.readAsDataURL(arquivo);
      var pos = arquivo.name.search('\.(ogg|wav|mp3)$');
      var r_name = RegExp('(_|/)', 'g');
      var r_ordem = RegExp('^([0-9]+ -|[0-9]+-|[0-9]+.)', 'g');
      var nome = arquivo.name.substring(0, pos).replace(r_name, ' ');
      var nome = nome.split(r_ordem);
      if(nome.length > 1) {
        var ordem = parseInt(nome[1].replace('-', '').trim());
        $("#id_nome").val(nome[2].trim());
        $("#id_ordem").val(ordem);
      } else {
        $("#id_nome").val(arquivo.name);
      }
    }
  });

  $("#btn-save").on({
    'click': function () {
      let nome = $("#id_nome").val();
      let album = $("#id_album").val();
      let ordem = $("#id_ordem").val();
      let base_arquivo = $("#file").val();
      let musica = {
        'nome': nome, 'album': album,
        'ordem': ordem, 'arquivo': base_arquivo
      }

      $.ajax({
        url: '/api/v1/musicas',
        type: 'POST',
        data: musica,
        dataType: 'json',
        statusCode: {
          201: function (data) {
            data = JSON.parse(data);
            if(data.musica) {
              $('#btn-close').removeClass('btn-danger');
              $('#btn-close').addClass('btn-success');
              $("#modal-text").text('Música cadastrada com sucesso!');
            } else {
              $('#btn-close').removeClass('btn-success');
              $('#btn-close').addClass('btn-danger');
              $('#modal-text').text(data.erros.join(', '));
            }
            $('#addmusic').modal();
          },
          400: function (data) {
            data = JSON.parse(data.responseJSON);
            $('#btn-close').addClass('btn-danger');
            $('#modal-text').text(data.erros.join(', '));
            $('#addmusic').modal();
          },
          404: function () {
            $('#btn-close').addClass('btn-warning');
            $('#modal-text').text('Erro ao acessar a api');
            $('#addmusic').modal();
          }
        }
      });
    }
  })
});
