$(function() {
  $('.date').datetimepicker({
    language: 'en',
    pick12HourFormat: true,
    pickSeconds: false,
  });

  $(".toggle_btn").tooltip();

  function toggle(what) {
    id=$(what).data("id");

    $.post("/admin/announcements/"+id+"/toggle/", function(data) {
      if(data[0]["success"]) {
        console.log("dim-wit twat");
        if($(what).hasClass("btn-default")) {
          $(what).removeClass("btn-default")
                 .addClass("btn-orange")
                 .html('<i class="fa fa-check"></i>')
                 .tooltip('hide')
                 .attr("title", "Enabled")
                 .tooltip('fixTitle')
                 .tooltip('show');
        } else {
          $(what).removeClass("btn-orange")
                 .addClass("btn-default")
                 .html('<i class="fa fa-times"></i>')
                 .tooltip('hide')
                 .attr("title", "Disabled")
                 .tooltip('fixTitle')
                 .tooltip('show');
        }
      }
    });
  };

  $(".toggle_btn").click(function(){
    if($(this).hasClass("btn-orange")) {
      toggle(this);
    } else {
      var yesno = confirm("Are you sure you want to activate this announcement?");

      if(yesno) {
        toggle(this);
      };
    }
  });
});
