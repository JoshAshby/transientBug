$ = jQuery

$.fn.check_form = (options) ->
  $(@).each (i, el) ->
    d = $(el).data("tb.check_form")

    if not d
      $(el).data("tb.check_form", (data = new FormChecker(el, options)))

    if typeof options is "string"
      d[options]()

class FormChecker
  constructor: (el, opts) ->
    @el = null
    @opts = null
    @init(el, opts)

  init: (element, @opts) ->
    @el = $ $(element).find "button:submit"

    @el.on "click", (e) ->
      e.preventDefault()
      errors = ""
      for input in $(@).parents("form").find "input"
        do (input) ->
          input = $ input
          if input.hasClass "has-error"
            errors += "#{ input.attr "name" } needs to be changed. #{ input.data "reason" }<br>"
      if errors
        $(@).parents("form").find("div.alert-danger").remove()
        $(@).parents("form").prepend """
        <div class="alert alert-danger">
          <b>Hold it.</b> Please fix these errors: <br>
          #{ errors }
        </div>
        """
      else
        $(@).parents("form").submit()
