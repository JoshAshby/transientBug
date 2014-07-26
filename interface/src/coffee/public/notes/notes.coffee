$ ->
  tags_tmpl = """ <p><span class="label label-red">{{tag}}</span></p> """
  tags_handlebars = Handlebars.compile tags_tmpl

  notes_tmpl = """
  <p class="note-typeahead" data-short="{{short_code}}">
    <i>{{title}}</i><br>
    <b>Tags:</b> {{#tags}} <span class="label label-red">{{this}}</span> {{/tags}}<br>
  </p>
  """
  notes_handlebars = Handlebars.compile notes_tmpl

  if $().typeahead? and Bloodhound?
    tags = new Bloodhound
      datumTokenizer: (d) ->
        Bloodhound.tokenizers.nonword d.tag
      queryTokenizer: Bloodhound.tokenizers.whitespace
      limit: 5
      prefetch:
        url: '/api/v0/notes/tags'
        filter: (list) ->
          $.map list[0]["tags"], (tag) ->
            {tag: tag, search: "tags:#{ tag }"}

    notes = new Bloodhound
      datumTokenizer: (d) ->
        d = "#{ d.title } #{ d.tags}"
        Boolhound.tokenizers.nonword d
      queryTokenizer: Bloodhound.tokenizers.whitespace
      limit: 5
      remote:
        url: '/api/v0/notes/search?s=%QUERY'
        filter: (d) ->
          $.map d[0]["pail"], (e) ->
            e["display"] = "note:#{ e.short_code }"
            e

    tags.initialize()
    notes.initialize()

    $("#search").typeahead null, {
        name: "notes"
        displayKey: "display"
        source: notes.ttAdapter()
        templates:
          header: """ <b>Notes</b> """
          suggestion: notes_handlebars
      }, {
        name: "tags"
        displayKey: "search"
        source: tags.ttAdapter()
        templates:
          header: """ <b>Tags</b> """
          suggestion: tags_handlebars
      }

  Mousetrap.bind 's', (e) ->
    e.preventDefault()
    $("#search").focus()
    $("#search").val ""
    if $().typeahead? and Bloodhound?
      $("#search").typeahead "val", ""

  $(document).on "click", ".note-typeahead", (e) ->
    short = $(@).data "short"
    window.location.href = "/notes/#{ short }"
