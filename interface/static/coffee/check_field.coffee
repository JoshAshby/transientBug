$ = jQuery

$.fn.check_field = (options) ->
  $(@).each (i, el) ->
    d = $(el).data("tb.check_field")

    if not d
      $(el).data("tb.check_field", (data = new FieldChecker(el, options)))

    if typeof options is "string"
      d[options]()

class FieldChecker
  default:
    url: ""
    return_name: "status"
    return_value: false
    reason: ""
    default: ""

  constructor: (el, opts) ->
    @el = null
    @opts = null
    @init(el, opts)

  init: (element, opts) ->
    @el = $ element
    @opts = $.extend {}, @default, opts
    @opts.default = @el.val()

    if $().done_typing?
      @el.done_typing
        on_done: =>
          @check()
        on_empty: =>
          @reset()

  check: () ->
    val = @el.val()
    if val isnt @opts.default
      $.getJSON @opts.url, name: val, (data) =>
        if data[0][@opts.return_name] is @opts.return_value
          @good()
        else
          @error()
    else
      @reset()

  error: () ->
    @el.parents("div.form-group")
      .removeClass("has-success")
      .addClass("has-error")
      .data("reason", @opts.reason)
      .find("span").remove()
    @el.parents("div.form-group")
      .append("""<span class="help-block">#{ @opts.reason }</span>""")

  good: () ->
    @el.parents("div.form-group")
      .removeClass("has-error")
      .addClass("has-success")
      .data("reason", "")
      .find("span").remove()

  reset: () ->
    @el.parents("div.form-group")
      .removeClass("has-success")
      .removeClass("has-error")
      .data("reason", "")
      .find("span").remove()
