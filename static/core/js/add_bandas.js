$(document).ready( function (){
  $("#id_band_image").on({
    'change': function () {
      var imagem = document.getElementById('id_band_image').files[0];
      var reader = new FileReader();
      reader.onload = function () {
        $("#file").val(reader.result);
      }
      reader.readAsDataURL(imagem);
    }
  });
  $("#btn-save").on({
    'click': function () {
      var nome = $("#id_name").val();
      var base_imagen = $("#file").val();
      var genero = $("#id_genre").val();
      var banda = {
        'name': nome, 'band_image': base_imagen, 'genre_id': genero
      }
      $.ajax({
        url: '/api/v1/banda',
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
