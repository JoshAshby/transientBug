$ ->
  $("#del_btn").click (e) ->
    e.preventDefault()
    yesno = confirm "Are you sure you want to delete this note?"

    if yesno
      img = $(this).data "short"
      $.post "/notes/#{ img }/delete", (data) ->
        if data[0]["success"]
          window.location.href="/notes"

  $("#quick_note_tags").pillbox
    url: "/notes/json/tags"
    name: "note"
    theme: "red"

$("#toc").tocify
  context: '.note-body'
  showEffect: 'none'
  showEffectSpeed: 'fast'

$("#toc").affix
    offset:
      top: 100
      bottom: 200
