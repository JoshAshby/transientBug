# bootstrap-fileinput.cofee
#
# JoshAshby <joshuaashby@joshashby.com>
#
# A rewrite and extension of the bootstrap-file-input.js
# Uses a fair deal of code/ideas behind the orig
#
# Difference:
#   - The layout of the resulting HTML is slightly different, along with the
#       rearanging of several CSS classes
#   - This has basic support for adding additional commands, through the usual
#      $().bootstrapFileInput('wat') format that are familiar with other
#      plugins. This is done by attaching itself to the "tb.fileinput" data
#      attribute on the element
$ = jQuery

$.fn.bootstrapFileInput = (options) ->
  $(@).each (i, el) ->
    d = $(el).data("tb.fileinput")

    if not d
      $(el).data("tb.fileinput", (data = new FileInputConverter(el, options)))

    if typeof options is "string"
      d[options]()

class FileInputConverter
  default_options:
    classes: "btn btn-default"
    title: "Browse"

  constructor: (el, opts) ->
    @els = null
    @opts = null
    @init(el, opts)

  init: (element, opts) ->
    @opts = $.extend {}, @default_options, opts
    @els = $ element
    @els.each (i, el) =>
      el = $ el

      # Make sure that we should actually style the input
      if el.data("bfi-disable")?
        return

      # If the input defines its own title, use it
      # This should be able to support using HTML within
      # the title, also
      if not el.data("title")?
        title = @opts.title
      else
        title = el.data "title"

      # Make a copy of the input
      clone = $('<div>').append(el.eq(0).clone()).html()

      # Make the wrapper element
      input_wrapper = $ '<div class="file-input-wrapper">'

      # Add the classes, keeping those from the input
      classes = "#{ @opts.classes } "
      classes += el.attr 'class' if not el.attr('class')?

      # Make the actual btn that "replaces" the input
      input_wrapper.append @btn classes, title, clone

      el.replaceWith input_wrapper

    .promise().done ->
      # Copied then moded to coffeescript from the orig plugin
      $('.file-input-wrapper').mousemove (cursor) ->
        # After we have found all of the file inputs let's apply a
        # listener for tracking the mouse movement.
        # This is important because the in order to give the illusion
        # that this is a button in FF we actually need to move the
        # button from the file input under the cursor. Ugh.
        # As the cursor moves over our new Bootstrap button we need
        # to adjust the position of the invisible file input Browse
        # button to be under the cursor.
        # This gives us the pointer cursor that FF denies us
        #
        # This wrapper element (the button surround this file input)
        wrapper = $ this
        # The invisible file input element
        input = wrapper.find "input[type=file]"
        # The left-most position of the wrapper
        wrapperX = wrapper.offset().left
        # The top-most position of the wrapper
        wrapperY = wrapper.offset().top
        # The with of the browsers input field
        inputWidth= input.width()
        # The height of the browsers input field
        inputHeight= input.height()
        # The position of the cursor in the wrapper
        cursorX = cursor.pageX
        cursorY = cursor.pageY

        # The positions we are to move the invisible file input
        # The 20 at the end is an arbitrary number of pixels that
        # we can shift the input such that cursor is not pointing
        # at the end of the Browse button but somewhere nearer
        # the middle
        moveInputX = cursorX - wrapperX - inputWidth + 20
        # Slides the invisible input Browse button to be positioned
        # middle under the cursor
        moveInputY = cursorY - wrapperY - (inputHeight/2)

        # Apply the positioning styles to actually move the
        # invisible file input
        input.css
          left:moveInputX
          top:moveInputY

      # Update the filename attribute once there is a change to the file input
      $('.file-input-wrapper input[type=file]').change (e) ->
        el = $ this
        fileName = el.val()

        if el.prop('files')? and el.prop('files').length > 1
          fileName = el[0].files.length+' files'
        else
          fileName = fileName.substring fileName.lastIndexOf('\\')+1, fileName.length

        el.parents(".file-input-wrapper").find("input[type=text]").val fileName

  btn: (classes, title, clone) ->
    """
    <div class="input-group file-input-group">
      <span class="input-group-btn file-input-group-btn">
        <a class="file-input-btn #{ classes }">#{ title }#{ clone }</a>
      </span>
      <input type="text" class="form-control file-input-name" value="No File Selected" readonly>
    </div>
    """

# Add the styles before the first stylesheet
# This ensures they can be easily overridden with developer styles
css = """
<style>
  .file-input-wrapper {
    overflow: hidden;
    position: relative;
    cursor: pointer;
  }

  .file-input-wrapper input[type=file],
  .file-input-wrapper input[type=file]:focus,
  .file-input-wrapper input[type=file]:hover {
    position: absolute;
    top: 0;
    left: 0;
    cursor: pointer;
    opacity: 0;
    filter: alpha(opacity=0);
    z-index: 99;
    outline: 0;
  }
</style>
"""

$('link[rel=stylesheet]').eq(0).before css
