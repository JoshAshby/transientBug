$ ->
  Mousetrap.bind 's', (e) ->
    e.preventDefault()
    $("#search").focus()
    $("#search").val ""

  tags = new Bloodhound
    datumTokenizer: (d) ->
      Bloodhound.tokenizers.nonword d.tag
    queryTokenizer: Bloodhound.tokenizers.whitespace
    limit: 10
    prefetch:
      url: '/api/v0/phots/tags'
      filter: (list) ->
        $.map list[0]["tags"], (tag) ->
          {tag: tag}

  tags.initialize()

  $('.search').typeahead null,
    {name: 'phottags'
    displayKey: "tag"
    source: tags.ttAdapter()}

  $("#views").on "change", "input[type=radio]", (e) ->
    e.preventDefault()
    b = $ this
    a = URI()
    a.setSearch "v", b.val()
    window.location.href = a.build()

  # Who said anything about eggs?
  sehll = () ->
    c = [
      "success"
      "info"
      "warning"
      "danger"
    ]
    c[Math.floor(Math.random()*c.length)]


  growl_options =
    type: sehll()
    ele: ".phots-collection"
    offset: 75
    position:
      from: "top"
      align: "center"
    template:
      container: "<div class=\"col-xs-10 col-sm-10 col-md-8 alert growl-animated growl-mouseover\">"

  syellayell = (msg) ->
    $.growl msg, growl_options

  choose_syell = (who) ->
    switch who
      when "c2dyYWNl"
        syells = [
          "I still don't understand fizzy water. Water tastes just fine without the CO2."
          "Interbutts is being slow."
          "WAY TO GO JOSH"
          "My legs... They burn!"
          "I smell bad... So... I'm gonna go take a shower then go to work."
          "That was awkward."
          "Fix the div or whatever!"
          "Thanks JoshAshby. My quotes, out of context, are immortalized in your world."
        ]
      when "aGlseQ=="
        syells = [
          "that sounded like a scoff, was that a scoff?"
          "whys everybody always ddo's on me?"
          "earmuffs, JoshAshby!"
        ]
    syells[Math.floor(Math.random()*syells.length)]

  $("#search").parents("form").on "submit", (e) ->
    val = $("#search").val().toLowerCase()
    if val
      ev = Base64.encode val
      switch ev
        when "c2dyYWNl", "aGlseQ=="
          e.preventDefault()
          syell = choose_syell(ev)
          syellayell syell

  #imgs = $(".phots-collection").find("img")

  #imgs.each (i, e) ->
    #console.log e
    #orig_src = e.src
    #c = document.createElement('canvas')
    #w = c.width = e.width
    #h = c.height = e.height
    #c.getContext('2d').drawImage(e, 0, 0, w, h)

    #$(e).data({src: orig_src, pause: c.toDataURL("image/gif")})

    #$(e).mouseenter ->
      #@.src = $(@).data("src")

    #$(e).mouseleave ->
      #@.src = $(@).data("pause")

    #e.src = c.toDataURL("image/gif")
