new_step = """
<div class="form-group">
  <label for="step-#{ step_counter }" class="sr-only"></label>
  <div class="row">
    <div class="col-md-11">
      <textarea class="form-control step" name="steps" data-order="#{ step_counter }" rows=10></textarea>
    </div>
    <div class="col-md-1">
      <button class="remove-step" class="btn btn-default"><i class="fa fa-times"></i></button>
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

step_counter = 1

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
    #$("#recipe-tags").pillbox url: "/api/v0/recipes/tags", name: "recipes"

    #file_upload =  $ '#phot_file'
    #file_upload.bootstrapFileInput()

    growl_options =
      position:
        from: "bottom"
        align: "right"
      template:
        container: '<div class="col-xs-10 col-sm-10 col-md-4 alert">'

    #list.find('input[type=checkbox]').bootstrapSwitch()

    reorder_steps = () ->
      step = 0
      $(".steps").each (e, i) ->
        $(e).data "order", step
        step++

    $("#add-step").click (e) ->
      e.preventDefault()
      $("#steps").append new_step
      step_counter++

    $("#steps").on "click", "button.remove-step", (e) ->
      e.preventDefault()
      yn = confirm "Are you sure you want to remove this step?"
      if yn
        $(@).parents("div.form-group").next().remove() # remove the br
        $(@).parents("div.form-group").remove()
        reorder_steps()

    $("#add-ingredient").click (e) ->
      e.preventDefault()
      $("#ingredients").append

    $("#ingredients").on "click", "button", (e) ->
      e.preventDefault()
      $(@).parents("div.input-group").next().remove() # get the br too
      $(@).parents("div.input-group").remove()
