LazyLoad.js [
  '/static/js/lib/bootstrap-growl.min.js'
], ->
    $ ->
      growl_options =
        position:
          from: "bottom"
          align: "right"
        template:
          container: '<div class="col-xs-10 col-sm-10 col-md-4 alert">'

      resend = (what, val) ->
        id = $(what).data "email"

        $.post "/admin/emails/#{ id }", (data) ->
          if data[0]["success"]
            $.growl "Invite email resent!<br><small>#{ id }</small>", growl_options

      $(".resend-invite").click ->
        resend this
