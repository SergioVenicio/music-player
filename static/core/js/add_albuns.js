$(document).ready( function (){
  $("#id_capa").on({
    'change': function () {
      var imagem = document.getElementById('id_capa').files[0];
      var reader = new FileReader();
      reader.onload = function () {
        $("#file").val(reader.result);
      }
      reader.readAsDataURL(imagem);
    }
  });
  $("#btn-save").on({
    'click': function () {
      var nome = $("#id_nome").val();
      var banda_id = $("#id_banda").val();
      var data_lancamento = $("#id_banda").val();
      var base_imagen = $("#file").val();
      var album = {
        'nome': nome, 'banda_id': banda_id,
        'data_lancamento': data_lancamento, 'capa': base_imagen
      }
      $.ajax({
        url: '/api/v1/album',
        type: 'POST',
        dataType: 'json',
        data: album ,
        statusCode: {
          201: function(data) {
            data = JSON.parse(data);
            if(data.album) {
              $('#btn-close').removeClass('btn-danger');
              $('#btn-close').addClass('btn-success');
              $("#modal-text").text('Banda cadastrado com sucesso!');
            } else {
              $('#btn-close').removeClass('btn-success');
              $('#btn-close').addClass('btn-danger');
              $('#modal-text').text(data.erros.join(', '));
            }
            $('#add_bandas').modal();
          },
          400: function(data) {
            data = JSON.parse(data.responseJSON);
            $('#btn-close').addClass('btn-danger');
            $('#modal-text').text(data.erros.join(', '));
            $('#add_bandas').modal();
          },
          404: function () {
            $('#btn-close').addClass('btn-warning');
            $('#modal-text').text('Erro ao acessar a api');
            $('#add_bandas').modal();
          }
        }
      });
    }
  });
});
