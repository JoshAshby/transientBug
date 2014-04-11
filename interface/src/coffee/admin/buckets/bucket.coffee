LazyLoad.css [
  '/static/css/lib/bootstrap-switch.min.css'
]

LazyLoad.js [
  '/static/js/lib/moment.min.js'
  '/static/js/lib/bootstrap-switch.min.js'
  '/static/js/lib/bootstrap-growl.min.js'
], ->
    $ ->
      growl_options =
        position:
          from: "bottom"
          align: "right"
        template:
          container: '<div class="col-xs-10 col-sm-10 col-md-4 alert">'

      $('input[type=checkbox]').bootstrapSwitch()

      $('input[type=checkbox]').on 'switch-change', (e, data) ->
        toggle this

      toggle = (what, val) ->
        id = $(what).data "id"

        $.post "/admin/buckets", {id: id}, (data) ->
          if data[0]["success"]
            wording = "shut off"
            if $(what).bootstrapSwitch 'state'
              wording = "activated"
            $.growl "Announcement #{ wording }!<br><small>#{ id }</small>", growl_options
