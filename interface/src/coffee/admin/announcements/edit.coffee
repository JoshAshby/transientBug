LazyLoad.css [
  '/static/css/lib/bootstrap-datetimepicker.min.css'
  '/static/css/lib/bootstrap-markdown.min.css'
  '/static/css/lib/bootstrap-switch.min.css'
]

LazyLoad.js [
  '/static/js/lib/moment.min.js'
  '/static/js/lib/bootstrap-datetimepicker.min.js'
  '/static/js/lib/bootstrap-markdown.js'
  '/static/js/lib/bootstrap-switch.min.js'
], ->
    $ ->
      form = $("#quick_announcement_edit")
      form.find('input[type=checkbox]').bootstrapSwitch()

      form.find('.date').datetimepicker
        language: 'en'
        pick12HourFormat: true
        pickSeconds: false

      start = form.find('#start')
      end   = form.find('#end')

      start_time_load = start.find("input").data("time")
      if start_time_load
        start_time_load = moment.unix(start_time_load)
        start.data("DateTimePicker").setDate start_time_load

      end_time_load = end.find("input").data("time")
      if end_time_load
        end_time_load = moment.unix(end_time_load)
        end.data("DateTimePicker").setDate end_time_load

      start.on "change.dp", (e) ->
        end.data("DateTimePicker").setStartDate e.date

      end.on "change.dp", (e) ->
        start.data("DateTimePicker").setEndDate e.date

      form.find("button:submit").on "click", (e) ->
        e.preventDefault()

        has_start_time = start.find("input").val()
        if has_start_time
          start_time = start.data("DateTimePicker").getDate()
          start.find("input").val start_time.unix()

        has_end_time = end.find("input").val()
        if has_end_time
          end_time = end.data("DateTimePicker").getDate()
          end.find("input").val end_time.unix()

        $(this).parents("form").submit()
