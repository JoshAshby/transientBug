$ ->
    labels = []
    labelsTemplate = """ <span class="label label-info">{{label}}</span> """
    labelsCompiledTemplate = Handlebars.compile labelsTemplate
    ###
    The hidden label may have labels preloaded, so we need to make sure
    those labels get into the array and the div list
    ###
    base = $("#addInputHidden").val()
    if base isnt ""
        labels = $.secureEvalJSON base
        for label in labels
            $("#dynamicList").append labelsCompiledTemplate {"label": label}

    ###
    Refresh the labels array and adding anything in the
    input box to the span
    ###
    refreshLabels = ->
        input = $("#addInputField").val()
        if input isnt ""
            ###
            #So long as the input field ins't empty, strip all spaces from the
            #input then break it into an array, by commas followed by merging
            #it with the existing array of labels, then we reduce it, removing
            #duplicates and finally push it to the template and hidden input
            #field
            ###
            labels_input_break = input.replace /\s+/g, ''
            labels_input_break = labels_input_break.split ","
            labels_input_break = labels_input_break.concat labels
            reduceSet = {}
            labels_input_reduced = []
            for label in labels_input_break
                reduceSet[label] = true
            for label of reduceSet
                labels_input_reduced.push label
            labels = labels_input_reduced
            $("#dynamicList").html ""
            for label in labels
                $("#dynamicList").append labelsCompiledTemplate {"label": label}
            $("#addInputHidden").val $.toJSON labels
            $("#addInputField").val ""


    ###
    When the add button is clicked then add the labels to the
    div list, the array and the hidden value, before finally
    clearing the field
    ###
    $("#addButton").click ->
        refreshLabels()

    ###
    Prevent the form from submitting if the enter key is pressed
    Instead, add the tags that are in the input
    ###
    $("#addInputField").keypress (event) =>
        if event.which is 13
            event.preventDefault()
            refreshLabels()

    ###
    Bind the click even to all labels
    When a click happens then remove that element
    from both the DOM and the array of labels and the hidden input
    ###
    $(document).on "click", "#dynamicList>span.label", ->
        labels.splice labels.indexOf($(this).text()), 1
        $("#addInputHidden").val $.toJSON labels
        $(this).remove()
