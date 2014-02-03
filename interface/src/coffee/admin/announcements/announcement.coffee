LazyLoad.js [
  '/static/js/admin/announcements/edit.js'
  '/static/js/admin/announcements/list.js'
  '/static/js/lib/mousetrap.min.js'
], ->
    Mousetrap.bind 'n', (e) ->
      e.preventDefault()
      $("ul.nav a[href=#new]").tab 'show'
      $('textarea[name="message"]').focus()

    Mousetrap.bind 'v', ->
      $("ul.nav a[href=#view]").tab 'show'
