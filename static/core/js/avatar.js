$(document).ready( function (){
  $("#avatar-error-modal").modal();
  var old_avatar = $("#avatar_previous").attr('src');
  $('#avatar_previous').addClass('hide');

  function readURL(file) {
    if (file) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#avatar_previous').attr('src', e.target.result);
            $(".avatar").attr('src', e.target.result);
        }

        reader.readAsDataURL(file);
    }
  }

  $("#id_avatar").change(function(){
      readURL(this.files[0]);
  });

  if($("#id_avatar").val()) {
    $('#file-info').html($("#id_avatar").val());
  }
  $("#id_avatar").on({
    'change': function () {
      $('#file-info').html($(this).val());
    }
  });
  $(".previous_clear").on({
    click: function () {
      $("#avatar_previous").attr('src', old_avatar);
      $(".avatar").attr('src', old_avatar);
      $('#file-info').text("");
    }
  });
});
