$ ->
    $(".bucketToggleButton").click ->
        console.log this
        elem = $(this)
        bucket = elem.parents("tr").attr "id"
        console.log bucket

        title = "Toggle this bucket?"
        text = "You are about to toggle the status of bucket <code>#{ bucket }</code>. Are you sure you want to do this?"

        callback = () ->
            $.post "/flagpole/dev/buckets/toggle/"+bucket, (data) ->
                if data["status"] is "200 OK"
                    if elem.hasClass "btn-inverse"
                        elem.removeClass "btn-inverse"
                        elem.addClass "btn-success"
                        elem.html "<i class=\"icon-bolt\"></i> Enabled"
                    else if elem.hasClass "btn-success"
                        elem.addClass "btn-inverse"
                        elem.removeClass "btn-success"
                        elem.html "<i class=\"icon-off\"></i> Disabled"
                    elem = $("#"+bucket+"ModalButton")
                    if elem.hasClass "btn-inverse"
                        elem.removeClass "btn-inverse"
                        elem.addClass "btn-success"
                        elem.html "<i class=\"icon-bolt\"></i> Enabled"
                    else if elem.hasClass "btn-success"
                        elem.addClass "btn-inverse"
                        elem.removeClass "btn-success"
                        elem.html "<i class=\"icon-off\"></i> Disabled"

        mod = new toggleModal title, text, callback
        mod.make()
