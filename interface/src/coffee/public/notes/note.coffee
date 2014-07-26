$ ->
  $("#del_btn").click (e) ->
    e.preventDefault()
    yesno = confirm "Are you sure you want to delete this note?"

    if yesno
      img = $(this).data "short"
      $.post "/notes/#{ img }/delete", (data) ->
        if data[0]["success"]
          window.location.href="/notes"

  $("#quick_note").find("input[type=checkbox]").bootstrapSwitch()
    .bootstrapSwitch 'setOnLabel', 'Yes'
    .bootstrapSwitch 'setOffLabel', 'No'

  $("#quick_note_tags").pillbox
    url: "/api/v0/notes/tags"
    name: "note"
    theme: "red"

  $("#toc").tocify
    context: '.note-body'
    showEffect: 'none'
    showEffectSpeed: 'fast'

  $("#toc").affix
      offset:
        top: 150
        bottom: 200

  Mousetrap.bind 'v', ->
    $("ul.nav a[href=#view]").tab 'show'

  Mousetrap.bind 'e', ->
    $("ul.nav a[href=#edit]").tab 'show'
