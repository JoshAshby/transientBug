$ ->
    ###
    When the user presses the delete button, generate the modal, throw it into
    the page and hope for the best.
    ###
    $(".requestDeleteButton").click ->
        email = $(this).data "email"
        id = $(this).parent("tr").data "id"
        text = "You're about to delete a persons one chance at getting into the fla.gr system! Just kidding, go a head and delete them, but don't expect anymore lemons after this!"
        title = "Delete request by `#{ email }`?"

        callback = () ->
          $.post "flagpole/requests/delete/"+id, ->

        mod = new deleteModal title, text, callback
        mod.make()


    ###
    When the user presses the grant button, generate the modal, throw it into
    the page and hope for the best. Just like deletes
    ###
    $(".requestGrantButton").click ->
        email = $(this).data "email"
        id = $(this).parent("tr").data "id"
        text = "Congrats! You're granting one persons dream of getting to use fla.gr while it's still closed! Good for you, you deserve more lemons!"
        title = "Grant request by `#{ email }`?"

        callback = () ->
          $.post "/flagpole/requests/grant/"+id, ->

        mod = new grantModal title, text, callback
        mod.make()


    $("#deleteAllButton").click ->
        values = []
        for box in $(".bulkCheckbox:checked")
            values.push $(box).val()

        text = "You're about to delete all of these requests! Are you sure you want to take this oppertunity away from all of these poor souls?"
        title = "Delete all of these?"

        callback = () ->
          for box in $(".bulkCheckbox:checked")
            id = $(box).val()
            $.post "/flagpole/requests/delete/"+id, ->

        mod = new deleteModal title, text, callback
        mod.make()


    $("#grantAllButton").click ->
        text = "You're about to grant all of these requests, which will send each and every person a specialized email for each one will be sent and they will all have an oppertunity to register for a closed trial account. Continue?"
        title = "Grant all of these?"

        callback = () ->
          for box in $(".bulkCheckbox:checked")
            id = $(box).val()
            $.post "/flagpole/requests/grant/"+id, ->


        mod = new grantModal title, text, callback
        mod.make()
