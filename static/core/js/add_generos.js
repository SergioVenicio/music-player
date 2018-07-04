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
      var descricao = $("#id_descricao").val();
      var base_imagem = $("#file").val();
      var genero = {
        'descricao': descricao,
        'imagem': base_imagem
      }
      $.ajax({
        url: '/api/v1/genero',
        type: 'POST',
        dataType: 'json',
        data: genero ,
        statusCode: {
          201: function(data) {
            data = JSON.parse(data);
            if(data.genero) {
              $('#btn-close').removeClass('btn-danger');
              $('#btn-close').addClass('btn-success');
              $("#modal-text").text('Genero cadastrado com sucesso!');
            } else {
              $('#btn-close').removeClass('btn-success');
              $('#btn-close').addClass('btn-danger');
              $('#modal-text').text(data.erros.join(', '));
            }
            $('#add_generos').modal();
          },
          400: function(data) {
            data = JSON.parse(data.responseJSON);
            $('#btn-close').addClass('btn-danger');
            $('#modal-text').text(data.erros.join(', '));
            $('#add_generos').modal();
          },
          404: function () {
            $('#btn-close').addClass('btn-warning');
            $('#modal-text').text('Erro ao acessar a api');
            $('#add_generos').modal();
          }
        }
      });
    }
  });
});
