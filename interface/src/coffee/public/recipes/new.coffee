new_step = (count) ->
  """
  <div class="form-group">
    <label for="steps">Step <span class="step-number">#{ count }</span></label>
    <a href="#" class="insert-step-before">Insert Empty Step Before</a>
    <a href="#" class="remove-step pull-right">Remove</a>
    <textarea class="form-control step" name="steps" data-step="#{ count }" rows=5></textarea>
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

    $("#recipe-tags").pillbox url: "/api/v0/recipes/tags", name: "recipe_tags", theme: "purple"

    #file_upload =  $ '#phot_file'
    #file_upload.bootstrapFileInput()

    $("#new-recipe").find('input[type=checkbox]').bootstrapSwitch()

    relabel_steps = () ->
      steps = $("#steps").find "div.form-group"
      steps.each (i, e) ->
        $el = $(e)
        $el.find("span.step-number").html i
        $el.find("textarea.step").data "step", i

    $("#add-step").click (e) ->
      e.preventDefault()
      $el = $ "#steps"
      count = $el.find("textarea.step").last().data "step"
      $el.append new_step count+1

    $(document).on "click", "a.insert-step-before", (e) ->
      e.preventDefault()
      $el = $ $(@).parents("div.form-group")
      $el.before new_step
      relabel_steps()

    $(document).on "click", "a.remove-step", (e) ->
      e.preventDefault()
      yn = confirm "Are you sure you want to remove this step?"
      if yn
        steps = $("#steps").find "div.form-group"
        if steps.length isnt 1
          $el = $(@).parents "div.form-group"
          $el.next().remove() # br
          $el.remove()
          relabel_steps()
        else
          $el = $(@).parents("div.form-group").find "textarea"
          $el.val ""

    $("#add-ingredient").click (e) ->
      e.preventDefault()
      $("#ingredients").append new_ingredient

    $("#ingredients").on "click", "button", (e) ->
      e.preventDefault()
      ingrs = $("#ingredients").find "div.input-group"
      if ingrs.length isnt 1
        $el = $(@).parents "div.input-group"
        $el.next().remove() # br
        $el.remove()
      else
        $el = $(@).parents("div.input-group").find "input"
        $el.val ""

    $("#new-recipe").on "click", 'button[type="submit"]', (e) ->
      e.preventDefault()
      recipe = $("#new-recipe").serialize()

      #$form = $("#new-recipe")

      #for field in ["name", "tags"]
        #recipe[field] = $form.find("input[name=\"#{ field }\"]").val()

      #steps = {}
      #for step in $("#steps").find("textarea")
        #$step = $(step)
        #steps[$step.data("step")] = $step.val()

      #ingredients = []
      #for ingre in $("#ingredients").find('input[type="text"]')
        #$ingr = $(ingre)
        #ingredients.push $ingr.val()

      #recipe["ingredients"] = ingredients
      #recipe["steps"] = steps

      #console.log recipe

      $.post "/recipes/new", recipe, (data) ->
        console.log data
