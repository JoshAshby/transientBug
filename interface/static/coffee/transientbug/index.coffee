$ ->
  tags = $.ajax
    url: "/phots/json/tags"
    async: false

  $('#q').typeahead
    name: 'tag_search'
    local: tags.responseJSON[0]["tags"]
    limit: 10

  $(".twitter-typeahead").css "display", "block"
  $(".tt-dropdown-menu").css "top", "initial"
  $(".tt-hint").css "padding-top", "1px"

  $("#phot_tags").pillbox url: "/phots/json/tags", name: "phot"
  $("#note_tags").pillbox url: "/notes/json/tags", name: "note"

  $("#phot_name").check_field
    url: "/phots/json/names"
    reason: "That name is already in use."

  $("#quick_phot").check_form()
