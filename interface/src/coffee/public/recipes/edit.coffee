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
  '/static/css/lib/bootstrap-markdown.min.css'
]

LazyLoad.js [
  '/static/js/lib/typeahead.bundle.min.js'
  '/static/js/pillbox.js'
  '/static/js/lib/bootstrap-switch.min.js'
  '/static/js/lib/bootstrap-markdown.js'
  #'/static/js/bootstrap-fileinput.js'
  #'/static/js/lib/bootstrap-growl.min.js'
], ->
  $ ->
    #growl_options =
      #position:
        #from: "bottom"
        #align: "right"
      #template:
        #container: '<div class="col-xs-10 col-sm-10 col-md-4 alert">'

    #file_upload =  $ '#phot_file'
    #file_upload.bootstrapFileInput()

    $("#recipe-tags").pillbox url: "/api/v0/recipes/tags", name: "recipe_tags", theme: "purple", placeholder: "Recipe Tags..."

    $("#new-recipe").find('input[type=checkbox]').bootstrapSwitch()

    relabel_steps = () ->
      steps = $("#steps").find "div.form-group"
      steps.each (i, e) ->
        $el = $(e)
        $el.find("span.step-number").html i+1
        $el.find("textarea.step").data "step", i+1

    $("#add-step").click (e) ->
      e.preventDefault()
      $el = $ "#steps"
      count = $el.find("textarea.step").last().data "step"
      $el.append new_step count+1

    $("#steps").on "click", "a.insert-step-before", (e) ->
      e.preventDefault()
      $el = $ $(@).parents("div.form-group")
      $el.before new_step
      relabel_steps()

    $("#steps").on "click", "a.remove-step", (e) ->
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

    $("#ingredients").on "keydown", "input", (e) ->
      switch e.keyCode
        when 9, 13
          e.preventDefault()
          $("#ingredients").append new_ingredient
          $("#ingredients").last("div.input-group").find('input').focus()

    $("#steps").on "keydown", "input", (e) ->
      switch e.keyCode
        when 9, 13
          e.preventDefault()
          $el = $ "#steps"
          count = $el.find("textarea.step").last().data "step"
          $el.append new_step count+1

    if $().typeahead? and Bloodhound?
      tags = new Bloodhound
        datumTokenizer: (d) ->
          Bloodhound.tokenizers.nonword d.name
        queryTokenizer: Bloodhound.tokenizers.whitespace
        sorter: (a, b) ->
          if a.relevance is b.relevance
            0
          else if a.relevance < b.relevance
            1
          else
            -1
        limit: 10
        prefetch:
          url: "/static/json/countries.json"

      tags.initialize()

      $("#countries").typeahead null,
        {name: "countries"
        displayKey: "name"
        source: tags.ttAdapter()}
