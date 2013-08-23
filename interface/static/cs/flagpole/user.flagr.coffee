$ ->
    $("#userToggleButton").click ->
        form = $(this).parents "form"
        input = form.find 'input[name="disable"]'

        if input.val() is "False"
            action = "disable"
            val = "true"
        else
            action = "enable"
            val = "false"

        title = "Are you sure?"
        text = "You are about to #{ action } this user. Are you sure you want to do this?"

        callback = () ->
            input.val val
            form.submit()

        mod = new toggleModal title, text, callback
        mod.make()

    $("#userDeleteButton").click ->
        form = $(this).parents "form"
        id = form.data "id"
        form.attr "action", "/flagpole/users/delete/"+id

        title = "Delete user?"
        text = "This action cannot be undone. Once deleted, their account will no longer exist and they will not be able to log in again. Are you sure you want to do this?"

        callback = () ->
            form.submit()

        mod = new deleteModal title, text, callback
        mod.make()
