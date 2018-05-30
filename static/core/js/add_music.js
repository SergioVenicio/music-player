$(document).ready( function (){
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  $("#btn-save").on({
    'click': function () {
      let nome = $("#id_nome").val();
      let album = $("#id_album").val();
      let ordem = $("#id_ordem").val();
      let arquivo = document.getElementById('id_arquivo').files[0];
      let reader = new FileReader();
      reader.onload = function () {
        $("#file").val(reader.result);
      }
      reader.readAsDataURL(arquivo);
      let base_arquivo = $("#file").val();
      let token = $('meta[name="csrf-token"]').attr('content');

      let musica = {
        'nome': nome, 'album': album,
        'ordem': ordem, 'arquivo': base_arquivo
      }

      $.ajax({
        url: '/api_v1/musicas',
        type: 'POST',
        data: musica,
        dataType: 'json',
        statusCode: {
          201: function (data) {
            data = JSON.parse(data);
            if(data.musica) {
              $('#btn-close').addClass('btn-success');
              $("#modal-text").text('Música cadastrada com sucesso!');
            } else {
              $('#btn-close').addClass('btn-danger');
              $('#modal-text').text(data.erros.join(', '));
            }
            $('#addmusic').modal();
          },
          400: function (data) {
            console.log(data);
            
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
