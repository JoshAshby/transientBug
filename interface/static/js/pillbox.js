// Generated by CoffeeScript 1.5.0
(function() {
  var $, Pillbox;

  $ = jQuery;

  $.fn.pillbox = function(options) {
    return $(this).each(function(i, el) {
      var d, data;
      d = $(el).data("tb.pillbox");
      if (!d) {
        $(el).data("tb.pillbox", (data = new Pillbox(el, options)));
      }
      if (typeof options === "string") {
        return d[options]();
      }
    });
  };

  Pillbox = (function() {

    Pillbox.prototype["default"] = {
      url: "",
      field: "tags",
      placeholder: "",
      name: ""
    };

    function Pillbox(el, opts) {
      this.el = null;
      this.opts = null;
      this.pill = null;
      this.input = null;
      this.init_val = null;
      this.tags = {};
      this.init(el, opts);
    }

    Pillbox.prototype.init = function(element, opts) {
      var input_keypress, tag, tags, _i, _len, _ref,
        _this = this;
      this.el = $(element);
      this.opts = $.extend({}, this["default"], opts);
      this.init_val = this.el.val();
      this.el.hide();
      this.el.after("<div class=\"pillbox\"><input type=\"text\" placeholder=\"" + this.opts.placeholder + "\"/></div>");
      this.pill = this.el.next(".pillbox");
      this.input = this.pill.find("input");
      input_keypress = function(e) {
        var key, last;
        switch (e.keyCode) {
          case 13:
            e.preventDefault();
            _this.tags[_this.input.val().trim()] = true;
            _this.input.val("");
            return _this.refresh();
          case 8:
          case 46:
            if (_this.getCaretPosition(_this.input.get()[0]) === 0) {
              e.preventDefault();
              last = _this.pill.find("span.label").last();
              if (last != null) {
                key = last.text().trim();
                _this.tags[key] = false;
                return _this.refresh();
              }
            }
        }
      };
      _ref = this.init_val.split(",");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        tag = _ref[_i];
        this.tags[tag.trim()] = true;
      }
      this.refresh();
      this.input.on("keydown", input_keypress);
      this.pill.on("click", 'i[data-role="remove"]', function(e) {
        var key;
        key = $(e.target).parent().text().trim();
        return _this.remove(key);
      });
      this.pill.click(function() {
        return _this.input.focus();
      });
      if ($().typeahead != null) {
        tags = $.ajax({
          url: this.opts.url,
          async: false
        });
        return this.input.typeahead({
          name: this.opts.name + '_tags',
          local: tags.responseJSON[0][this.opts.field],
          limit: 10
        });
      }
    };

    Pillbox.prototype.refresh = function() {
      var status, tag, tags, text, _ref;
      text = "";
      tags = [];
      this.pill.find("span.label").remove();
      _ref = this.tags;
      for (tag in _ref) {
        status = _ref[tag];
        if (status && tag) {
          this.pill.prepend(" <span class=\"label label-theme\">" + tag + " <i data-role=\"remove\" class=\"fa fa-times\"></i></span> ");
          tags.push(tag);
        }
      }
      return this.el.val(tags.join(","));
    };

    Pillbox.prototype.remove = function(item) {
      if (item in this.tags) {
        this.tags[item] = false;
        return this.refresh();
      }
    };

    Pillbox.prototype.add = function(item) {
      this.tags[item] = true;
      return this.refresh();
    };

    Pillbox.prototype.empty = function() {
      this.tags = {};
      return this.refresh();
    };

    Pillbox.prototype.getCaretPosition = function(oField) {
      var iCaretPos, oSel;
      iCaretPos = 0;
      if (document.selection) {
        oField.focus();
        oSel = document.selection.createRange();
        oSel.moveStart('character', -oField.value.length);
        iCaretPos = oSel.text.length;
      } else if (oField.selectionStart || oField.selectionStart === '0') {
        iCaretPos = oField.selectionStart;
      }
      return iCaretPos;
    };

    return Pillbox;

  })();

}).call(this);
