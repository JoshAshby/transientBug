$ ->
  $("#del_btn").click (e) ->
    e.preventDefault()
    yesno = confirm "Are you sure you want to delete this note?"

    if yesno
      img = $(this).data "short"
      $.post "/notes/edit/#{ img }/delete", (data) ->
        if data[0]["success"]
          window.location.href="/notes"

  editor = new EpicEditor
    theme:
      base: 'css/lib/epic/base/epiceditor.css'
      preview: 'css/lib/epic/preview/github.css'
      editor: 'css/lib/epic/editor/epic-dark.css'
    basePath: '/static/'
    autogrow:
      minHeight: 200
    textarea: "content"
    button:
      preview: false
      fullscreen: false
  .load()

  editor.on 'update', ->
    $("#preview").html this.exportFile null, 'html'
  .emit 'update'

  $(document).on "sidebar-toggle", ->
    setTimeout ->
      editor.reflow()
    , 100

  $(document).on "sidebar-link", ->
    setTimeout ->
      editor.reflow()
    , 100

  $("#note_tags").pillbox url: "/notes/tags/json", name: "note"
