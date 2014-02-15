LazyLoad.js [
  '/static/js/lib/typeahead.bundle.min.js',
  '/static/js/lib/mousetrap.min.js',
], ->
  $ ->
    Mousetrap.bind 's', (e) ->
      e.preventDefault()
      $("#search").focus()
      $("#search").val ""

    posts = new Bloodhound
      datumTokenizer: (d) ->
        Bloodhound.tokenizers.whitespace d.title
      queryTokenizer: Bloodhound.tokenizers.whitespace
      limit: 10
      prefetch:
        url: '/api/v0/notes/'

    posts.initialize()

    $('.search').typeahead null,
      {name: 'posts'
      displayKey: 'title'
      source: posts.ttAdapter()}
