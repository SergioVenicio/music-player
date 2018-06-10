$(document).ready( function (){
  $("#signup-error-modal").modal();

  if($("#id_avatar").val()) {
    $('#file-info').html($("#id_avatar").val());
  }
  $("#id_avatar").on({
    'change': function () {
      $('#file-info').html($(this).val());
    }
  });
});
