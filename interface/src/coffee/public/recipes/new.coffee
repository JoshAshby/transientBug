new_step = (counter) ->
  """
  <div class="form-group">
    <label for="step-#{ counter }" class="step-number"></label>
    <div class="row">
      <div class="col-md-11">
        <textarea class="form-control step" name="steps" data-order="#{ counter }" rows=5></textarea>
      </div>
      <div class="col-md-1">
        <button class="remove-step btn btn-default"><i class="fa fa-times"></i></button>
      </div>
    </div>
  </div>
  <br>
  """

new_ingredient = """
<div class="input-group">
  <input type="text" class="form-control input-sm" name="ingredients" placeholder="Ingredient..." />
  <span class="input-group-btn">
    <button class="btn btn-default btn-sm"><i class="fa fa-times"></i></button>
  </span>
</div>
<br>
"""

LazyLoad.css [
  '/static/css/pillbox.css'
  '/static/css/lib/bootstrap-switch.min.css'
]

LazyLoad.js [
  '/static/js/lib/typeahead.bundle.min.js'
  '/static/js/pillbox.js'
  '/static/js/bootstrap-fileinput.js'
  '/static/js/lib/bootstrap-switch.min.js'
  '/static/js/lib/bootstrap-growl.min.js'
], ->
  $ ->
    #growl_options =
      #position:
        #from: "bottom"
        #align: "right"
      #template:
        #container: '<div class="col-xs-10 col-sm-10 col-md-4 alert">'

    #$("#recipe-tags").pillbox url: "/api/v0/recipes/tags", name: "recipes"

    #file_upload =  $ '#phot_file'
    #file_upload.bootstrapFileInput()

    $("#new-recipe").find('input[type=checkbox]').bootstrapSwitch()

    reorder_steps = () ->
      steps = $("#steps").find("div.form-group")
      if steps.length is 1
        steps.first().find("button.remove-step").hide()
      else
        steps.each (i, e) ->
          $el = $(e)
          $el.find("button.remove-step").show()
          $el.find("label.step-number").html "Step #{ i }"

    step_counter = 1

    $("#add-step").click (e) ->
      e.preventDefault()
      $("#steps").append new_step step_counter
      step_counter++
      reorder_steps()

    $("#steps").on "click", "button.remove-step", (e) ->
      e.preventDefault()
      yn = confirm "Are you sure you want to remove this step?"
      if yn
        $el = $(@).parents "div.form-group"
        $el.next().remove() # br
        $el.remove()
        reorder_steps()

    $("#add-ingredient").click (e) ->
      e.preventDefault()
      $("#ingredients").append new_ingredient

    $("#ingredients").on "click", "button", (e) ->
      e.preventDefault()
      $el = $(@).parents "div.input-group"
      $el.next().remove() # br
      $el.remove()
