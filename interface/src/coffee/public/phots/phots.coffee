$ ->
  if $().typeahead? and Bloodhound? and Handlebars?
    tags_tmpl = """ <p><span class="label label-green">{{tag}}</span></p> """
    tags_handlebars = Handlebars.compile tags_tmpl

    phots_tmpl = """
    <p class="phot-typeahead" data-short="{{short_code}}">
      <table>
        <tr>
          <td>
            <img height="50px" width="50px" src="/i/{{filename}}" />
          </td>
          <td>
            <i>{{title}}</i><br>
            <b>Tags:</b> {{#tags}} <span class="label label-green">{{this}}</span> {{/tags}}<br />
          </td>
        </tr>
      </table>
    </p>
    """
    phots_handlebars = Handlebars.compile phots_tmpl

    tags = new Bloodhound
      datumTokenizer: (d) ->
        Bloodhound.tokenizers.nonword d.tag
      queryTokenizer: Bloodhound.tokenizers.whitespace
      limit: 5
      prefetch:
        url: '/api/v0/phots/tags'
        filter: (list) ->
          $.map list[0].tags, (tag) ->
            tag = tag.replace(/_/g, ' ')
            {tag: tag, search: "tags:#{ tag }"}

    phots = new Bloodhound
      datumTokenizer: (d) ->
        d = "#{ d.title } #{ d.tags }"
        Bloodhound.tokenizers.nonword d
      queryTokenizer: Bloodhound.tokenizers.whitespace
      limit: 5
      remote:
        url: '/api/v0/phots/search?s=%QUERY'
        filter: (d) ->
          $.map d[0].pail, (e) ->
            e.display = "phot:#{ e.short_code }"
            e

    tags.initialize()
    phots.initialize()

    $('#search').typeahead null,
      {
        name: 'phot-tags'
        displayKey: 'tag'
        source: tags.ttAdapter()
        templates:
            header: '<b>Tags</b>'
            suggestion: tags_handlebars
      }, {
        name: 'phots',
        displayKey: 'display'
        source: phots.ttAdapter()
        teplates:
          header: '<b>Phots</b>'
          suggestion: phots_handlebars
      }

  Mousetrap.bind 's', (e) ->
    e.preventDefault()
    $("#search").focus()
    $("#search").val ""
    if $().typeahead? and Bloodhound? and Handlebars?
      $("#search").typeahead "val", ""

  $(document).on "click", ".phot-typeahead", (e) ->
    short = $(@).data "short"
    window.location.href = "/phots/#{ short }"

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
