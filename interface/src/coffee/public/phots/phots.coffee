LazyLoad.css [
  '/static/css/growl.css'
]

LazyLoad.js [
  '/static/js/lib/typeahead.bundle.min.js',
  '/static/js/lib/mousetrap.min.js',
  '/static/js/done_typing.js',
  '/static/js/lib/bootstrap-growl.min.js',
  '/static/js/lib/base64.js'
  '/static/js/lib/URI.js'
], ->
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
    growl_options =
      ele: ".phots-collection"
      offset: 75
      position:
        from: "top"
        align: "center"
      template:
        container: '<div class="col-xs-10 col-sm-10 col-md-8 alert growl-animated growl-mouseover">'

    syellayell = (msg) ->
      $.growl msg, growl_options

    choose_syell = () ->
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
      syells[Math.floor(Math.random()*syells.length)]

    $("#search").parents("form").on "submit", (e) ->
      val = $("#search").val()
      if val
        ev = Base64.encode val
        switch ev
          when "c2dyYWNl"
            e.preventDefault()
            syell = choose_syell()
            syellayell syell
