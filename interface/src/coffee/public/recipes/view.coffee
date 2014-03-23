LazyLoad.css [
  '/static/css/growl.css'
]

LazyLoad.js [
  '/static/js/lib/bootstrap-growl.min.js',
], ->
  $ ->
    growl_error =
      type: "danger"
      position:
        from: "top"
        align: "center"
      template:
        container: "<div class=\"col-xs-10 col-sm-10 col-md-8 alert growl-animated growl-mouseover\">"

    growl_okay = growl_error
    growl_okay.type = "info"

    $("#no-delete").click (e) ->
      e.preventDefault()
      $("ul.nav a[href=#view]").tab 'show'
      $.growl "Okay, okay, we <b>will not</b> delete this recipe.", growl_okay

    $("#yes-delete").click (e) ->
      e.preventDefault()

      $.ajax
        type: "DELETE"
        url: window.location.href
        success: (d) ->
          if d[0]["success"]
            window.location.href = "/recipes"
          else
            $.growl "There was a problem while attempting to delete that recipe. The error has been logged, and we're working on getting it fixed.", growl_options
