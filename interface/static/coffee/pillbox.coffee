$ = jQuery

$.fn.pillbox = (options) ->
  $(@).each (i, el) ->
    d = $(el).data("tb.pillbox")

    if not d
      $(el).data("tb.pillbox", (data = new Pillbox(el, options)))

    if typeof options is "string"
      d[options]()

class Pillbox
  default:
    url: ""
    field: "tags"
    placeholder: ""
    name: ""

  constructor: (el, opts) ->
    @el = null
    @opts = null
    @pill = null
    @input= null
    @init_val = null
    @tags = {}
    @init(el, opts)

  init: (element, opts) ->
    @el = $ element
    @opts = $.extend {}, @default, opts

    @init_val = @el.val()
    @el.hide()

    @el.after """<div class="pillbox"><input type="text" placeholder="#{ @opts.placeholder }"/></div>"""
    @pill = @el.next(".pillbox")
    @input = @pill.find("input")

    input_keypress = (e) =>
      switch e.keyCode
        when 13
          e.preventDefault()
          @tags[@input.val().trim()] = true
          @input.val ""
          @refresh()

        when 8, 46
          if @getCaretPosition(@input.get()[0]) is 0
            e.preventDefault()
            last = @pill.find("span.label").last()
            if last?
              key = last.text().trim()
              @tags[key]= false
              @refresh()

    for tag in @init_val.split(",")
      @tags[tag.trim()] = true
    @refresh()

    @input.on "keydown", input_keypress
    @pill.on "click", 'i[data-role="remove"]', (e) =>
      key = $(e.target).parent().text().trim()
      @remove(key)

    @pill.click =>
      @input.focus()

    if $().typeahead?
      tags = $.ajax url: @opts.url, async: false

      @input.typeahead
        name: @opts.name+'_tags'
        local: tags.responseJSON[0][@opts.field]
        limit: 10

  refresh: () ->
    text = ""
    tags = []
    @pill.find("span.label").remove()
    for tag, status of @tags
      if status and tag
        @pill.prepend """ <span class="label label-theme">#{ tag } <i data-role="remove" class="fa fa-times"></i></span> """
        tags.push tag

    @el.val tags.join ","

  remove: (item) ->
    if item of @tags
      @tags[item] = false
      @refresh()

  add: (item) ->
    @tags[item] = true
    @refresh()

  empty: () ->
    @tags = {}
    @refresh()

  getCaretPosition: (oField) ->
    iCaretPos = 0
    if document.selection
      oField.focus()
      oSel = document.selection.createRange()
      oSel.moveStart 'character', -oField.value.length
      iCaretPos = oSel.text.length
    else if oField.selectionStart or oField.selectionStart is '0'
      iCaretPos = oField.selectionStart
    iCaretPos
