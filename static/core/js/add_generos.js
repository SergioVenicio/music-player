$(document).ready( function (){
  $("#id_imagen").on({
    'change': function () {
      var imagen = document.getElementById('id_imagen').files[0];
      var reader = new FileReader();
      reader.onload = function () {
        $("#file").val(reader.result);
      }
      reader.readAsDataURL(imagen);
    }
  });
  $("#btn-save").on({
    'click': function () {
      var descricao = $("#id_descricao").val();
      var base_imagen = $("#file").val();
      var genero = {
        'descricao': descricao,
        'imagen': base_imagen
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
