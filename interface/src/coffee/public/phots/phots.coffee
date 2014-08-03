$ ->
  $("#views").on "change", "input[type=radio]", (e) ->
    e.preventDefault()
    b = $ this
    a = URI()
    a.setSearch "v", b.val()
    window.location.href = a.build()
