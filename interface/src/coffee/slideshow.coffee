LazyLoad.js [
  '/static/js/lib/bespoke-all.js'
  '/static/js/lib/mousetrap.min.js'
], ->
  $ ->
    slideshow = bespoke.from 'article',
      keys: true
      progress: true
      touch: true
      blackout: true
      hash: true

    Mousetrap.bind 'esc', ->
      old_url = window.location.toString()
      new_url = old_url.substring 0, old_url.indexOf '?'
      window.location = new_url
