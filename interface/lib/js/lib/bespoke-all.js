/*!
 * Bespoke.js v0.4.0
 *
 * Copyright 2014, Mark Dalgleish
 * This content is released under the MIT license
 * http://mit-license.org/markdalgleish
 */

(function(moduleName, window) {
	var from = function(selectorOrElement, selectedPlugins) {
			var parent = selectorOrElement.nodeType === 1 ? selectorOrElement : document.querySelector(selectorOrElement),
				slides = [].filter.call(parent.children, function(el) { return el.nodeName !== 'SCRIPT'; }),
				activeSlide = slides[0],
				listeners = {},

				activate = function(index, customData) {
					if (!slides[index]) {
						return;
					}

					fire('deactivate', createEventData(activeSlide, customData));

					activeSlide = slides[index];

					slides.map(deactivate);

					fire('activate', createEventData(activeSlide, customData));

					addClass(activeSlide, 'active');
					removeClass(activeSlide, 'inactive');
				},

				deactivate = function(el, index) {
					var offset = index - slides.indexOf(activeSlide),
						offsetClass = offset > 0 ? 'after' : 'before';

					['before(-\\d+)?', 'after(-\\d+)?', 'active', 'inactive'].map(removeClass.bind(null, el));

					el !== activeSlide &&
						['inactive', offsetClass, offsetClass + '-' + Math.abs(offset)].map(addClass.bind(null, el));
				},

				slide = function(index, customData) {
					if (arguments.length) {
						fire('slide', createEventData(slides[index], customData)) && activate(index, customData);
					} else {
						return slides.indexOf(activeSlide);
					}
				},

				step = function(offset, customData) {
					var slideIndex = slides.indexOf(activeSlide) + offset;

					fire(offset > 0 ? 'next' : 'prev', createEventData(activeSlide, customData)) && activate(slideIndex, customData);
				},

				on = function(eventName, callback) {
					(listeners[eventName] || (listeners[eventName] = [])).push(callback);

					return function() {
						listeners[eventName] = listeners[eventName].filter(function(listener) {
							return listener !== callback;
						});
					};
				},

				fire = function(eventName, eventData) {
					return (listeners[eventName] || [])
						.reduce(function(notCancelled, callback) {
							return notCancelled && callback(eventData) !== false;
						}, true);
				},

				createEventData = function(el, eventData) {
					eventData = eventData || {};
					eventData.index = slides.indexOf(el);
					eventData.slide = el;
					return eventData;
				},

				deck = {
					on: on,
					fire: fire,
					slide: slide,
					next: step.bind(null, 1),
					prev: step.bind(null, -1),
					parent: parent,
					slides: slides
				};

			addClass(parent, 'parent');

			slides.map(function(el) {
				addClass(el, 'slide');
			});

			for (var pluginName in selectedPlugins) {
				if (!plugins[pluginName]) {
					throw Error('Missing plugin: ' + moduleName + '-' + pluginName);
				}
				selectedPlugins[pluginName] !== false && plugins[pluginName](deck, selectedPlugins[pluginName]);
			}

			activate(0);

			decks.push(deck);

			return deck;
		},

		decks = [],

		plugins = {},

		addClass = function(el, cls) {
			el.classList.add(moduleName + '-' + cls);
		},

		removeClass = function(el, cls) {
			el.className = el.className
				.replace(RegExp(moduleName + '-' + cls +'(\\s|$)', 'g'), ' ')
				.trim();
		},

		callOnAllDecks = function(method) {
			return function() {
				var args = arguments;
				decks.map(function(deck) {
					deck[method].apply(null, args);
				});
			};
		};

	window[moduleName] = {
		from: from,
		slide: callOnAllDecks('slide'),
		next: callOnAllDecks('next'),
		prev: callOnAllDecks('prev'),
		plugins: plugins
	};

}('bespoke', window));
/*!
 * bespoke-blackout v0.0.1
 *
 * Copyright 2013, Luis Nell
 * This content is released under the MIT license
 * http://luis.mit-license.org/
 */

!(function(bespoke) {
    var BLACK_KEYCODE = 66,  // b key
        WHITE_KEYCODE = 87;  // w key

    var plugin = function() {
        var shown = false,
            overlay = document.createElement('div');

        overlay.id = 'bespoke-blackout';
        overlay.style.display = 'none';
        overlay.style.position = 'absolute';
        overlay.style.left = overlay.style.top = '0';
        overlay.style.zindex = 255;
        document.body.appendChild(overlay);

        window.addEventListener('keydown', function(e) {
            if (!shown &&
                (e.which === BLACK_KEYCODE || e.which === WHITE_KEYCODE)) {
                    shown = true;
                    overlay.style.background = e.which === BLACK_KEYCODE ? '#000' : '#fff';
                    overlay.style.display = 'block';
                    overlay.style.width = window.innerWidth + 'px';
                    overlay.style.height = window.innerHeight + 'px';
                    e.preventDefault();
            } else if (e.which === 27 || e.which === 13 ||
                       e.which === BLACK_KEYCODE ||
                       e.which === WHITE_KEYCODE) {
                overlay.style.display = 'none';
                shown = false;
                e.preventDefault();
            }
        });

        /* Sometimes it happens to me that I'm falling out of OSX fullscreen
         * mode by pressing ESC too often. This should keep everything
         * blacked/whiten out :) */
        window.addEventListener('resize', function() {
            if (!shown) {
                return;
            }
            overlay.style.width = window.innerWidth + 'px';
            overlay.style.height = window.innerHeight + 'px';
        });
    };

    bespoke.plugins.blackout = plugin;

}(bespoke));
/*!
 * bespoke-hash v0.1.2
 *
 * Copyright 2013, Mark Dalgleish
 * This content is released under the MIT license
 * http://mit-license.org/markdalgleish
 */

(function(bespoke) {

	bespoke.plugins.hash = function(deck) {
		var activeIndex,

			parseHash = function() {
				var hash = window.location.hash.slice(1),
					slideNumberOrName = parseInt(hash, 10);

				if (hash) {
					if (slideNumberOrName) {
						activateSlide(slideNumberOrName - 1);
					} else {
						deck.slides.forEach(function(slide, i) {
							slide.getAttribute('data-bespoke-hash') === hash && activateSlide(i);
						});
					}
				}
			},

			activateSlide = function(index) {
				if (index !== activeIndex) {
					deck.slide(index);
				}
			};

		setTimeout(function() {
			parseHash();

			deck.on('activate', function(e) {
				var slideName = e.slide.getAttribute('data-bespoke-hash');
				window.location.hash = slideName || e.index + 1;
				activeIndex = e.index;
			});

			window.addEventListener('hashchange', parseHash);
		}, 0);
	};

}(bespoke));/*!
 * bespoke-keys v0.1.0
 * https://github.com/markdalgleish/bespoke-keys
 *
 * Copyright 2013, Mark Dalgleish
 * This content is released under the MIT license
 */

bespoke.plugins.keys = function(deck, options) {
  var isHorizontal = options === true || options == 'horizontal';

  document.addEventListener('keydown', function(e) {
    (
      e.which == 34 || // PAGE DOWN
      e.which == 32 || // SPACE
      isHorizontal && e.which == 39 || // RIGHT
      !isHorizontal && e.which == 40 // DOWN
    ) && deck.next();
    (
      e.which == 33 || // PAGE UP
      isHorizontal && e.which == 37 || // LEFT
      !isHorizontal && e.which == 38 // UP
    ) && deck.prev();
  });
};
/*!
 * bespoke-progress v0.1.0
 * https://github.com/markdalgleish/bespoke-progress
 *
 * Copyright 2013, Mark Dalgleish
 * This content is released under the MIT license
 */

(function(bespoke) {

  bespoke.plugins.progress = function (deck, options) {
    var progressParent = document.createElement('div'),
      progressBar = document.createElement('div'),
      prop = options === 'vertical' ?
        'height' :
        ['horizontal', true].indexOf(options) + 1 ?
          'width' :
          undefined;

    if (!prop) {
      return;
    }

    progressParent.className = 'bespoke-progress-parent';
    progressBar.className = 'bespoke-progress-bar';
    progressParent.appendChild(progressBar);
    deck.parent.appendChild(progressParent);

    deck.on('activate', function(e) {
      progressBar.style[prop] = (e.index * 100 / (deck.slides.length - 1)) + '%';
    });
  };

}(bespoke));
/*!
 * bespoke-touch v0.1.0
 * https://github.com/markdalgleish/bespoke-touch
 *
 * Copyright 2013, Mark Dalgleish
 * This content is released under the MIT license
 */

bespoke.plugins.touch = function(deck, options) {
  var axis = options === true || options == 'horizontal' ? 'X' : 'Y',
    startPosition,
    delta;

  deck.parent.addEventListener('touchstart', function(e) {
    if (e.touches.length == 1) {
      startPosition = e.touches[0]['page' + axis];
      delta = 0;
    }
  });

  deck.parent.addEventListener('touchmove', function(e) {
    if (e.touches.length == 1) {
      e.preventDefault();
      delta = e.touches[0]['page' + axis] - startPosition;
    }
  });

  deck.parent.addEventListener('touchend', function() {
    Math.abs(delta) > 50 && (delta > 0 ? deck.prev() : deck.next());
  });
};
