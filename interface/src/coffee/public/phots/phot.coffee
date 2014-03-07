LazyLoad.css [
  '/static/css/pillbox.css'
  '/static/css/lib/bootstrap-switch.min.css'
]

LazyLoad.js [
  '/static/js/lib/typeahead.bundle.min.js'
  '/static/js/pillbox.js'
  '/static/js/bootstrap-fileinput.js'
  '/static/js/lib/bootstrap-switch.min.js'
  '/static/js/lib/bootstrap-growl.min.js'
], ->
  $ ->
    $("#phot_tags").pillbox url: "/api/v0/phots/tags", name: "phot"

    file_upload =  $ '#phot_file'
    file_upload.bootstrapFileInput()

    list = $ '#phot_collection'
    growl_options =
      position:
        from: "bottom"
        align: "right"
      template:
        container: '<div class="col-xs-10 col-sm-10 col-md-4 alert">'

    list.find('input[type=checkbox]').bootstrapSwitch()

    list.find('input[type=checkbox]').on 'switch-change', (e, data) ->
      toggle this

    toggle = (what, val) ->
      id = $(what).data "id"

      $.post "/admin/phots/#{ id }", {state: val}, (data) ->
        if data[0]["success"]
          wording = "enabled"
          if data[0]["state"]
            wording = "disabled"
          $.growl "Phot #{ wording }!<br><small>#{ id }</small>", growl_options
