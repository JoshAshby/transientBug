$(function() {
  $("#del_btn").click(function() {
    var yesno = confirm("Are you sure you want to delete this note?");

    if(yesno) {
      var img=$(this).data("short");

      $.post("/notes/edit/delete/"+img, function(data) {
        if(data[0]["data"]["success"]) {
          window.location.href="/notes";
        }
      });
    };
  });

  $("#save_btn").click(function(e) {
    e.preventDefault();
    var id=$(this).data("short");
    var form=$(this).parents("form").serialize();
    $.post("/notes/edit/update/"+id, form, function(data) {
      if(data[0]["data"]["success"]) {
        window.location.reload();
      };
    });
  });
});
