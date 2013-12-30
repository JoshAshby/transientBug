// Generated by CoffeeScript 1.5.0
(function() {
  var $, FieldChecker;

  $ = jQuery;

  $.fn.check_field = function(options) {
    return $(this).each(function(i, el) {
      var d, data;
      d = $(el).data("tb.check_field");
      if (!d) {
        $(el).data("tb.check_field", (data = new FieldChecker(el, options)));
      }
      if (typeof options === "string") {
        return d[options]();
      }
    });
  };

  FieldChecker = (function() {

    FieldChecker.prototype["default"] = {
      url: "",
      return_name: "status",
      return_value: false,
      reason: "",
      "default": ""
    };

    function FieldChecker(el, opts) {
      this.el = null;
      this.opts = null;
      this.init(el, opts);
    }

    FieldChecker.prototype.init = function(element, opts) {
      var _this = this;
      this.el = $(element);
      this.opts = $.extend({}, this["default"], opts);
      this.opts["default"] = this.el.val();
      if ($().done_typing != null) {
        return this.el.done_typing({
          on_done: function() {
            return _this.check();
          },
          on_empty: function() {
            return _this.reset();
          }
        });
      }
    };

    FieldChecker.prototype.check = function() {
      var val,
        _this = this;
      val = this.el.val();
      if (val !== this.opts["default"]) {
        return $.getJSON(this.opts.url, {
          name: val
        }, function(data) {
          if (data[0][_this.opts.return_name] === _this.opts.return_value) {
            return _this.good();
          } else {
            return _this.error();
          }
        });
      } else {
        return this.reset();
      }
    };

    FieldChecker.prototype.error = function() {
      this.el.parents("div.form-group").removeClass("has-success").addClass("has-error").data("reason", this.opts.reason).find("span").remove();
      return this.el.parents("div.form-group").append("<span class=\"help-block\">" + this.opts.reason + "</span>");
    };

    FieldChecker.prototype.good = function() {
      return this.el.parents("div.form-group").removeClass("has-error").addClass("has-success").data("reason", "").find("span").remove();
    };

    FieldChecker.prototype.reset = function() {
      return this.el.parents("div.form-group").removeClass("has-success").removeClass("has-error").data("reason", "").find("span").remove();
    };

    return FieldChecker;

  })();

}).call(this);