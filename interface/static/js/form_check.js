// Generated by CoffeeScript 1.5.0
(function() {
  var $, FormChecker;

  $ = jQuery;

  $.fn.check_form = function(options) {
    return $(this).each(function(i, el) {
      var d, data;
      d = $(el).data("tb.check_form");
      if (!d) {
        $(el).data("tb.check_form", (data = new FormChecker(el, options)));
      }
      if (typeof options === "string") {
        return d[options]();
      }
    });
  };

  FormChecker = (function() {

    function FormChecker(el, opts) {
      this.el = null;
      this.opts = null;
      this.init(el, opts);
    }

    FormChecker.prototype.init = function(element, opts) {
      this.opts = opts;
      this.el = $($(element).find("button:submit"));
      return this.el.on("click", function(e) {
        var errors, input, _fn, _i, _len, _ref;
        e.preventDefault();
        errors = "";
        _ref = $(this).parents("form").find("input");
        _fn = function(input) {
          input = $(input);
          if (input.hasClass("has-error")) {
            return errors += "" + (input.attr("name")) + " needs to be changed. " + (input.data("reason")) + "<br>";
          }
        };
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          input = _ref[_i];
          _fn(input);
        }
        if (errors) {
          $(this).parents("form").find("div.alert-danger").remove();
          return $(this).parents("form").prepend("<div class=\"alert alert-danger\">\n  <b>Hold it.</b> Please fix these errors: <br>\n  " + errors + "\n</div>");
        } else {
          return $(this).parents("form").submit();
        }
      });
    };

    return FormChecker;

  })();

}).call(this);