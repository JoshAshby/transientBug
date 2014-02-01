$ ->
  slideshow = remark.create ratio: '16:9'

  setTimeout reset_css, 500

reset_css = () ->
  $('.remark-slide-scaler').css
    'box-shadow': 'None'
    '-webkit-box-shadow': 'None'
    '-moz-box-shadow': 'None'
