LazyLoad.css [
  '/static/css/pillbox.css'
]

LazyLoad.js [
  '/static/js/lib/typeahead.bundle.min.js'
  '/static/js/pillbox.js'
  #'/static/js/done_typing.js'
  #'/static/js/check_field.js'
  #'/static/js/form_check.js'
  '/static/js/bootstrap-fileinput.js'
], ->
  $ ->
    toggle = (what) ->
      id = $(what).data "id"
      di = $("#"+id)

      $.post "/admin/phots/#{ id }/toggle", (data) ->
        if data[0]["success"]
          window.location.reload()

    $("#phot_tags").pillbox url: "/api/v0/phots/tags", name: "phot"

    #$("#phot_name").check_field
      #url: "/phots/json/names"
      #reason: "That name is already in use."

    #$("#phot_name").done_typing
      #wait_interval: 1500
      #on_done: ->
        #$("#phot_name").check_field("check")
      #on_empty: ->
        #$("#phot_name").check_field("reset")

    #$("#quick_phot").check_form()

    file_upload =  $ '#phot_file'
    file_upload.bootstrapFileInput()
