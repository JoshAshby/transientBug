$ ->
  $("#add_group").click (e) ->
    e.preventDefault()
    $("#groups").append """
      <div class="input-group">
        <input type="text" class="form-control input-sm" name="groups" placeholder="Group..." />
        <span class="input-group-btn">
          <button class="btn btn-default btn-sm"><i class="fa fa-times"></i></button>
        </span>
      </div>
      <br>
      """

  $("#groups").on "click", "button", (e) ->
    e.preventDefault()
    if $(@).parents("div.input-group").find("input").val() in ["root", "admin"]
      yn = confirm "Are you sure you want to remove this group? Doing so could be dangerous"

      if yn
        $(@).parents("div.input-group").next().remove() # get the br too
        $(@).parents("div.input-group").remove()
    else
        $(@).parents("div.input-group").next().remove() # get the br too
        $(@).parents("div.input-group").remove()
