$(function() {
  function toggle(what) {
    id=$(what).data("id");

    $.post("/admin/phots/toggle/"+id, function(data) {
      if(data[0]["data"]["success"]) {
        $(what).popover('hide'); // hmm
        $(what).slideUp();
      };
    });
  };

  $(document).on("click", ".confirm_btn", function() {
    toggle(this);
  });

  $(".toggle_btn").click(function(){
    if($(this).hasClass("btn-theme")) {
      var title = "Disable?";
    } else {
      var title = "Enable?";
    };

    var id = $(this).data("id");

    $(this).popover({trigger: "manual",
      placement: "bottom",
      html: true,
      title: title,
      content: '<div class="btn-group"><button class="btn btn-success confirm_btn" data-id="'+id+'"><i class="icon-ok"></i></button><button class="btn btn-default nope_btn"><i class="icon-remove"></i></button></div>',
      container: "body"});
    $(this).popover('show');

    var wat = this;
    setTimeout(function() {
      $(wat).popover('hide');
    }, 2000);
  });
});
