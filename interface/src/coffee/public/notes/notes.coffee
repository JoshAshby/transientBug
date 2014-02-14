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
        url: '/notes/json/posts'
        filter: (list) ->
          $.map list[0]["posts"], (post) ->
            {title: post.title}

    posts.initialize()

    $('.search').typeahead null,
      {name: 'Posts'
      displayKey: 'title'
      source: posts.ttAdapter()}
