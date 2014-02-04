LazyLoad.js [
  '/static/js/bootstrap-fileinput.js'
], ->
  $ ->
    file_upload = $ '#scrn_upload'
    file_upload.bootstrapFileInput()

    $(".del_btn").click ->
      yesno = confirm "Are you sure you want to delete this screenshot?"

      if yesno
        img = $(this).data "img"

        $.post "/screenshots/#{ img }/delete/", (data) ->
          if data[0]["success"]
            window.location.href = "/screenshots"
