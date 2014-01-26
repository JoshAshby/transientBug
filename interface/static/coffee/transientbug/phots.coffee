$ ->
  tags = $.ajax
    url: "/phots/json/tags"
    async: false

  $('#q').typeahead
    name: 'tag_search'
    local: tags.responseJSON[0]["tags"]
    limit: 10

  $("#views").click ->
    setTimeout ->
      $("#views").parents("form").submit()
    , 100
