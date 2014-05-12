LazyLoad.css [
  '/static/css/lib/bootstrap-switch.min.css'
]

LazyLoad.js [
  '/static/js/lib/moment.min.js'
  '/static/js/lib/bootstrap-switch.min.js'
  '/static/js/lib/bootstrap-growl.min.js'
], ->
    $ ->
      list = $('#announcement_list')
      growl_options =
        position:
          from: "bottom"
          align: "right"
        template:
          container: '<div class="col-xs-10 col-sm-10 col-md-4 alert">'

      list.find('input[type=checkbox]').bootstrapSwitch()

      list.find('input[type=checkbox]').on 'switch-change', (e, data) ->
        toggle this

      toggle = (what, val) ->
        id = $(what).data "id"

        $.post "/admin/announcements/#{ id }/toggle", {state: val}, (data) ->
          if data[0]["success"]
            wording = "shut off"
            if data[0]["state"]
              wording = "activated"
            $.growl "Announcement #{ wording }!<br><small>#{ id }</small>", growl_options

      now = moment()
      list.find(".time").each (index, elem) ->
        el = $ elem
        time = el.data "time"
        msg = el.data "msg"
        if time
          time = moment.unix time
          if time.isAfter(now)
            ending = "s"
          else
            ending = "d"
          el.html "#{ msg }#{ ending } on: #{ time.format 'MMM Do (ddd), YYYY' } at #{ time.format 'hh:mm A' }<br>"
