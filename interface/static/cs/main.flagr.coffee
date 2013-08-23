$ ->
    ###
    Setup the various focus events for the forms in the dropdown menus...
    ###
    $("#dropdownSearchToggle").click ->
        setTimeout ->
            $("#dropdownSearchInput").focus()
        , 10

    $("#dropdownLoginToggle").click ->
        setTimeout ->
            $("#dropdownLoginEmail").focus()
        , 10

    $("#dropdownLoginEmail").keypress (event) =>
        if event.which is 13
            event.preventDefault()
            setTimeout ->
                $("#dropdownLoginPassword").focus()
            , 10


    $("#checkAllButton").click ->
        if $(this).hasClass 'active'
            $(".bulkCheckbox").prop 'checked', false
        else
            $(".bulkCheckbox").prop 'checked', true
