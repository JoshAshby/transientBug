LazyLoad.css [
  '/static/css/pages/recipes/recipes.css'
]

LazyLoad.js [
  '/static/js/lib/typeahead.bundle.min.js'
  '/static/js/lib/handlebars-v1.3.0.js'
  '/static/js/lib/mousetrap.min.js'
], ->
  $ ->
    tags_tmpl = """ <p><span class="label label-purple">{{tag}}</span></p> """
    tags_handlebars = Handlebars.compile tags_tmpl

    recipes_tmpl = """
    <p class="recipe-typeahead" data-short="{{short_code}}">
      <i>{{title}}</i><br>
      <b>Tags:</b> {{#tags}} <span class="label label-purple">{{this}}</span> {{/tags}}<br>
      <b>Country:</b> {{country}}
    </p>
    """
    recipes_handlebars = Handlebars.compile recipes_tmpl

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
              {tag: tag, search: "tags:#{ tag }"}

      recipes = new Bloodhound
        datumTokenizer: (d) ->
          d = "#{ d.title } #{ d.tags} #{ d.description}"
          Bloodhound.tokenizers.nonword d
        queryTokenizer: Bloodhound.tokenizers.whitespace
        limit: 5
        remote:
          url: '/api/v0/recipes/search?s=%QUERY'
          filter: (d) ->
            $.map d[0]["pail"], (e) ->
              e["display"] = "recipe:#{ e.short_code }"
              e

      tags.initialize()
      countries.initialize()
      recipes.initialize()

      $("#search").typeahead null, {
          name: "recipes"
          displayKey: "display"
          source: recipes.ttAdapter()
          templates:
            header: """ <b>Recipes</b> """
            suggestion: recipes_handlebars
        }, {
          name: "countries"
          displayKey: "name"
          source: countries.ttAdapter()
          templates:
            header: """ <b>Countries</b> """
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

    $(document).on "click", ".recipe-typeahead", (e) ->
      short = $(@).data "short"
      window.location.href = "/recipes/#{ short }"
