$ ->
    ###
    When a delete button is pressed, grab the id and title of the flag
    from the data-id and data-title attributes of the button, then use
    the compiled Handlebars template from above to generate the modal
    and finally put it into the page and display it
    ###
    $(".deleteButton").click ->
        id = $(this).data "id"
        title = $(this).data "title"
        action = $(this).data "action"

        title = "Delete: #{ title }?"
        text = "You're about to delete your flag `#{ title }`<br> Doing so will delete it forever, are you sure you want to continue?"

        callback = () ->
            $.post action, ->

        mod = new deleteModal title, text, callback
        mod.make()
