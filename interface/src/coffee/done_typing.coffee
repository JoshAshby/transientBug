$ = jQuery

$.fn.extend
  done_typing: (options) ->
    self = $.fn.done_typing
    opts = $.extend {}, self.default_options, options

    $(@).each (i, el) ->
      self.init el, opts

$.extend $.fn.done_typing,
  default_options:
    wait_interval: 2000
    on_done: null
    on_empty: null

  init: (_el, opts) ->
    @_el = $(_el)
    @_opts = opts
    @_timeout_id = null

    @build()

  build: () ->
    self = @
    @_el.keyup ->
      clearTimeout self._timeout_id

      if $(@).val()
        self._timeout_id = setTimeout ->
          self.done self
        , self._opts.wait_interval
      else
        self._timeout_id = setTimeout ->
          self.empty self
        , self._opts.wait_interval

  done: (self) ->
    $.event.trigger
      type: "done_typing-paused"
      element: self._el

    if self._opts.on_done?
      self._opts.on_done()

  empty: (self) ->
    $.event.trigger
      type: "done_typing-empty"
      element: self._el

    if self._opts.on_empty?
      self._opts.on_empty()
