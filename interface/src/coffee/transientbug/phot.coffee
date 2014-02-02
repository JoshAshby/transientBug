$ ->
  timeout = null

  toggle = (what) ->
    id = $(what).data "id"
    di = $("#"+id)

    $.post "/admin/phots/#{ id }/toggle", (data) ->
      if data[0]["success"]
        window.location.reload()

  $(document).on "click", ".confirm_btn", ->
    toggle this

  $(document).on "click", ".nope_btn", ->
    $(".toggle_btn").popover 'hide'

  $(".toggle_btn").click (e) ->
    e.preventDefault()
    id = $(this)
    $(".toggle_btn").not(this).popover 'hide'
    $(this).popover 'show'
    $(".popover").find(".confirm_btn").data "id", $(this).data "id"

    timeout = setTimeout ->
      id.popover 'hide'
    , 3000

    $(document).on "mouseenter", ".popover", ->
      clearTimeout timeout
    .on "mouseleave", ".popover", ->
      timeout = setTimeout ->
        id.popover 'hide'
      , 3000

  .popover
    trigger: "manual"
    placement: "auto right"
    html: true
    content: '<div class="btn-group"><button class="btn btn-success btn-sm confirm_btn"><i class="fa fa-check"></i></button><button class="btn btn-default btn-sm nope_btn"><i class="fa fa-times"></i></button></div>'
    container: "body"

  $("#phot_tags").pillbox url: "/phots/json/tags", name: "phot"

  $("#phot_name").check_field
    url: "/phots/json/names"
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
    for input in $(@).parents("form").find("input")
      do (input) ->
        input = $ input
        if input.hasClass "has-error"
          errors += "#{ input.attr "name" } needs to be changed. #{ input.data "reason" }<br>"
    if errors
      $(@).parents("form").prepend """
      <div class="alert alert-danger"><b>Hold it.</b> Please fix these errors: <br>
        #{ errors }
      </div>
      """
    else:
      $(@).parents("form").submit()
