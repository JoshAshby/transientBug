$ ->
  tags = $.ajax
    url: "/phots/tags/json"
    async: false

  $('#q').typeahead
    name: 'tag_search'
    local: tags.responseJSON[0]["tags"]
    limit: 10

  $(".twitter-typeahead").css "display", ""
  $(".tt-dropdown-menu").css "top", "initial"
  $(".tt-hint").css "padding-top", "1px"

  $("#phot_tags").pillbox url: "/phots/tags/json", name: "phot"
  $("#note_tags").pillbox url: "/notes/tags/json", name: "note"

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

  $("#phot_name").check_field
    url: "/phots/names/json"
    reason: "That name is already in use."

  $("#phot_name").done_typing
    wait_interval: 1500
    on_done: ->
      $("#phot_name").check_field("check")
    on_empty: ->
      $("#phot_name").check_field("reset")

  $("#new_phot").click (e) ->
    errors = ""
    e.preventDefault()
    for input in $(@).parents("form").find "input"
      do (input) ->
        input = $ input
        if input.hasClass "has-error"
          errors += "#{ input.attr "name" } needs to be changed. #{ input.data "reason" }<br>"
    if errors
      $(@).parents("form").prepend """
      <div class="alert alert-danger">
        <b>Hold it.</b> Please fix these errors: <br>
        #{ errors }
      </div>
      """
    else
      $(@).parents("form").submit()

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
