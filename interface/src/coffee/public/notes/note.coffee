LazyLoad.css [
  '/static/css/pillbox.css'
  '/static/css/tocify.css'
  '/static/css/lib/bootstrap-markdown.min.css'
  '/static/css/lib/bootstrap-switch.min.css'
]

LazyLoad.js [
  '/static/js/pillbox.js'
  '/static/js/lib/typeahead.bundle.min.js'
  '/static/js/lib/bootstrap-markdown.js'
  '/static/js/lib/jquery-ui-1.9.1.custom.min.js'
  '/static/js/lib/jquery-tocify.min.js'
  '/static/js/lib/mousetrap.min.js'
  '/static/js/lib/bootstrap-switch.min.js'
], ->
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
          top: 100
          bottom: 200

    Mousetrap.bind 'v', ->
      $("ul.nav a[href=#view]").tab 'show'

    Mousetrap.bind 'e', ->
      $("ul.nav a[href=#edit]").tab 'show'

    Mousetrap.bind 's s', ->
      old_url = window.location.toString()
      new_url = old_url.substring 0, old_url.indexOf '?'
      window.location = new_url+"?v=slideshow"
