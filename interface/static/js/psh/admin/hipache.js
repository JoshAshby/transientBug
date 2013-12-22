// Generated by CoffeeScript 1.5.0
(function() {

  $(function() {
    $("#add_route").click(function(e) {
      e.preventDefault();
      return $("#routes").append("<div class=\"input-group\">\n  <input type=\"text\" class=\"form-control\" name=\"domains\" Placeholder=\"Domain...\" />\n  <span class=\"input-group-btn\">\n    <button class=\"btn btn-default remove_route\"><i class=\"fa fa-times\"></i></button>\n  </span>\n</div>\n<br>");
    });
    $("#routes").on("click", ".remove_route", function(e) {
      e.preventDefault();
      $(this).parents("div.input-group").next().remove();
      return $(this).parents("div.input-group").remove();
    });
    return $("#remove").click(function() {
      var id, yn;
      id = $(this).data("id");
      yn = confirm("Are you sure you want to delete this route?");
      if (yn) {
        return $.post("/admin/hipache/" + id + "/delete", function(data) {
          if (data[0]["status"] === "success") {
            return window.location = "/admin/hipache";
          }
        });
      }
    });
  });

}).call(this);
