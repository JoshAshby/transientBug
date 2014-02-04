LazyLoad.js [
  '/static/js/public/phots/phots.js'
  '/static/js/public/phots/phot.js'
  '/static/js/public/notes/note.js'
  '/static/js/public/scrns/scrn.js'
  '/static/js/lib/masonry.min.js'
], ->
  $ ->
    setTimeout ->
      $("#wall").masonry
        itemSelector: '.brick'
        columnWidth: '.brick'
    , 1000
