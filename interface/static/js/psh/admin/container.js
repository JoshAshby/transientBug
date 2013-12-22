// Generated by CoffeeScript 1.5.0
(function() {

  $(function() {
    var id, toggle;
    id = $("#container-id").val();
    $("#disable").click(function() {
      var yn;
      yn = confirm("Are you sure you want to disable this container?");
      if (yn) {
        return toggle();
      }
    });
    $("#enable").click(function() {
      return toggle();
    });
    return toggle = function() {
      $.post("/admin/containers/" + id + "/disable");
      return window.location.reload();
    };
  });

}).call(this);
