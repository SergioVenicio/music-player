$(document).ready( function (){
  $("#id_cover_image").on({
    'change': function () {
      var imagem = document.getElementById('id_cover_image').files[0];
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
      var banda_id = $("#id_band").val();
      var data_lancamento = $("#id_release_date").val();
      var base_imagen = $("#file").val();
      var album = {
        'name': nome,
        'band_id': banda_id,
        'release_date': data_lancamento,
        'cover_image': base_imagen
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
