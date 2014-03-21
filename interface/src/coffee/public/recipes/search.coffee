LazyLoad.css [
  '/static/css/pages/recipes/recipes.css'
]

LazyLoad.js [
  '/static/js/lib/typeahead.bundle.min.js'
  '/static/js/lib/handlebars-v1.3.0.js'
  '/static/js/lib/mousetrap.min.js'
], ->
  $ ->
    if $().typeahead? and Bloodhound?
      countries = new Bloodhound
        datumTokenizer: (d) ->
          Bloodhound.tokenizers.nonword d.name
        queryTokenizer: Bloodhound.tokenizers.whitespace
        sorter: (a, b) ->
          if a.relevance is b.relevance
            0
          else if a.relevance < b.relevance
            1
          else
            -1
        limit: 5
        prefetch:
          url: "/static/json/countries.json"

      tags = new Bloodhound
        datumTokenizer: (d) ->
          Bloodhound.tokenizers.nonword d.tag
        queryTokenizer: Bloodhound.tokenizers.whitespace
        limit: 5
        prefetch:
          url: '/api/v0/recipes/tags'
          filter: (list) ->
            $.map list[0]["tags"], (tag) ->
              {tag: tag}

      tags.initialize()
      countries.initialize()

      $("#search").typeahead null, {
          name: "countries"
          displayKey: "name"
          source: countries.ttAdapter()
          templates:
            header: """ <b>Countries</b> """
        }, {
          name: "tags"
          displayKey: "tag"
          source: tags.ttAdapter()
          templates:
            header: """ <b>Tags</b> """
            suggestion: Handlebars.compile """ <p><span class="label label-purple">{{tag}}</span></p> """
        }

    Mousetrap.bind 's', (e) ->
      e.preventDefault()
      $("#search").focus()
      $("#search").val ""
      if $().typeahead? and Bloodhound?
        $("#search").typeahead "val", ""
