$(document).ready( function (){
  $("#id_imagem").on({
    'change': function () {
      var imagem = document.getElementById('id_imagem').files[0];
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
      var base_imagen = $("#file").val();
      var genero = $("#id_genero").val();
      var banda = {
        'nome': nome, 'imagem': base_imagen, 'genero_id': genero
      }
      $.ajax({
        url: '/api_v1/banda',
        type: 'POST',
        dataType: 'json',
        data: banda ,
        statusCode: {
          201: function(data) {
            data = JSON.parse(data);
            if(data.genero) {
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
