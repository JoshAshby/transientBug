$(function() {
  $('.date').datetimepicker({
    language: 'en',
    pick12HourFormat: true,
    pickSeconds: false,
  });

  $(".toggle_btn").tooltip();
  function toggle(what) {
    id=$(what).data("id");

    $.post("/admin/announcements/toggle/"+id, function(data) {
      if(data[0]["data"]["success"]) {
        console.log("dim-wit twat");
        if($(what).hasClass("btn-default")) {
          $(what).removeClass("btn-default")
                 .addClass("btn-theme")
                 .html('<i class="icon-ok"></i>')
                 .data("title", "Enabled");
        } else {
          $(what).removeClass("btn-theme")
                 .addClass("btn-default")
                 .html('<i class="icon-remove"></i>')
                 .data("title", "Enabled");
        }
      }
    });
  };

  $(".toggle_btn").click(function(){
    if($(this).hasClass("btn-theme")) {
      toggle(this);
    } else {
      var yesno = confirm("Are you sure you want to activate this announcement?");

      if(yesno) {
        toggle(this);
      };
    }
  });
});
