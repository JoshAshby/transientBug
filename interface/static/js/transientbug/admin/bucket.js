$(function() {
  function toggle(what) {
    id=$(what).data("id");

    $.post("/admin/buckets/"+id+"/toggle/", function(data) {
      if(data[0]["success"]) {
        console.log("dim-wit twat");
        if($(what).hasClass("btn-default")) {
          $(what).removeClass("btn-default")
                 .addClass("btn-orange")
                 .html('<i class="fa fa-check"></i>');
        } else {
          $(what).removeClass("btn-orange")
                 .addClass("btn-default")
                 .html('<i class="fa fa-times"></i>');
        }
      }
    });
  };

  $(".toggle_btn").click(function(){
    if($(this).hasClass("btn-orange")) {
      toggle(this);
    } else {
      var yesno = confirm("Are you sure you want to activate this bucket?");

      if(yesno) {
        toggle(this);
      };
    }
  });
});
