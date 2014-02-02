$ ->
  # Open a given tab if its in the url
  url = document.location.toString()
  if url.match '#'
      $("ul.nav a[href=##{ url.split('#')[1] }]").tab 'show'

  $('ul.nav a').on 'shown.bs.tab', (e) ->
      if history.pushState
        history.pushState null, null, e.target.hash
      else
        window.location.hash = e.target.hash
