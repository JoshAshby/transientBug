$(function() {
  $("#del_btn").click(function(){
    var yesno = confirm("Are you sure you want to delete this image?");

    if(yesno) {
      img=$(this).data("img");

      $.post("/phots/edit/delete/"+img, function(data) {
        if(data[0]["data"]["success"]) {
          window.location.href="/phots";
        }
      });
    };
  });

  $("#pillbox").pillbox();

  var tags = $.ajax({url: "/phots/json/tags", async: false});

  $('.pillbox input').typeahead({
    name: 'phots_tags',
    local: tags.responseJSON[0]["data"],
    limit: 10
  });
});
