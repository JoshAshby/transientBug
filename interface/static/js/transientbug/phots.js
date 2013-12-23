// Generated by CoffeeScript 1.5.0
(function() {

  $(function() {
    var tags;
    tags = $.ajax({
      url: "/phots/tags/json",
      async: false
    });
    $('#q').typeahead({
      name: 'phots_tags',
      local: tags.responseJSON[0]["tags"],
      limit: 10
    });
    $("#views").click(function() {
      return setTimeout(function() {
        return $("#views").parents("form").submit();
      }, 100);
    });
    $('.thumbnail_h6').tooltip();
    $(".twitter-typeahead").removeAttr("style");
    $(".tt-dropdown-menu").css("top", "initial");
    return $(".tt-hint").css("padding-top", "1px");
  });

}).call(this);
