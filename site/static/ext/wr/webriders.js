/**
 * WebRiders Framework
 *
 * @version 0.5
 * @author Brizgunov Rostislav
 */
var WebRiders = WR = {
};

/**
 * Utility functions
 */
WebRiders.util = {
    /**
     * Create namespace or return existent.
     *
     * @param {String} name - namespace name. E.g. 'WR.CustomSite'
     *
     * @return {Object} - namespace object. May be not empty
     */
    namespace: function(name) {
        name = name.split('.');
        var c = window, n = '';
        while (n = name.shift()) {
            if (typeof c[n] == 'undefined')
                c[n] = {};
            c = c[n];
        }
        return c;
    },

    /**
     * Alias for the 'namespace' method
     */
    ns: function() {
        return this.namespace.apply(this, arguments);
    },

    /**
     * Load script dependencies
     *
     * @param {String/Array} scripts - path:
     *     "my/script.js"
     *     "my/script1.js my/script2.js"
     *     "my/script1.js, my/script2.js  my/script3.js ,    my/script4.js"
     *     ["my/script1.js", "my/script2.js", "my/script3.js"]
     * @param {Object} config
     *
     * @config {Function} callback. Not required
     * @config {*} context - callback context (scope) object. Not required
     * @config {Boolean} cache - true to leave URL unchanged. false to add '?_=12442432' to it. Default: false
     * @config {Boolean} async - true to load scripts asynchronous. Default: false
     */
    require: function(scripts, config) {
        scripts = scripts || '';
        config = config || {};

        if (typeof scripts == "string")
            scripts = scripts.replace(/^\s+|\s+$/g, '').replace(/\s*,\s*|\s+/g, ',').split(',');

        if (!$.isArray(scripts))
            return false;

        var loaded = this.require.loaded = this.require.loaded || {};

        for (var i = 0, l = scripts.length; i < l; i++) {
            var script = scripts[i] || '';
            if (script.search(/^https?:\/\//) !== 0) {
                var loc = window.location, path = '';
                if (script.indexOf('/') === 0)
                    path = window.location.protocol + '//' + window.location.host;
                else
                    path = (config.path || this.require.defaultPath || '');
                script = path + script;
            }

            if (!loaded[script]) {
                var success = function(data, textStatus) {
                    loaded[script] = true;
                    if (typeof config.callback == "function")
                        config.callback.apply(this, arguments);
                };

                $.ajax({
                    url: script,
                    dataType: 'script',
                    success: success,
                    context: config.context,
                    cache: !!config.cache,
                    async: !!config.async
                });
            }
        }

        return true;
    },

    /**
     * Get shuffled subset from the list
     *
     * @param {Array} list
     * @param {Number} cnt - how many elements should we get? Default: all
     */
    randomSample: function(list, cnt) {
        cnt = cnt || list.length;
        list = $.extend([], list);
        var new_list = [];
        while (cnt) {
            cnt--;
            new_list.push(list.splice(Math.round(Math.random() * (list.length - 1)), 1)[0]);
        }
        return new_list;
    }
}

/**
 * Simple string template
 * @param {String} source
 * @constructor
 */
WR.util.Template = function(source) {
    this.source = source;
};

WR.util.Template.prototype = {
    source: '',

    apply: function(config) {
        config = config || {};
        return this.source.replace(
            /{{\s*(.*?)\s*}}/g,
            function (a, b) {
                var r = config[b];
                if (typeof r == "undefined")
                  r = "";
                return r;
            }
        );
    }
};

/**
 * Little utility that adds to object events handling
 */
WR.util.eventable = function(obj, events) {
    // Enable some events
    obj.events = {};
    events = events || [];
    for (var i = 0, l = events.length; i < l; i++) {
        obj.events[events[i]] = [];
    }

    obj.bind = function(eventName, listener, scope) {
        if (!this.events[eventName])
            throw new Error("Event " + eventName + " is not implemented");

        if (scope)
            listener.customScope = scope;

        this.events[eventName].push(listener);
    };

    obj.unbind = function(eventName, listenerToRemove) {
        if (!this.events[eventName])
            throw new Error("Event " + eventName + " is not implemented");

        var listeners = this.events[eventName],
                newListeners = [];

        while (listeners.length) {
            var listener = listeners.shift();
            if (listener !== listenerToRemove) {
                newListeners.push(listener);
            }
        }

        this.events[eventName] = newListeners;
    };

    obj.trigger = function(eventName /* data1, data2, ... */) {
        if (!this.events[eventName])
            throw new Error("Event " + eventName + " is not implemented");

        var listenerReturn, eventReturn = true;
        for (var i = 0, listeners = this.events[eventName], l = listeners.length; i < l; i++) {
            var listener = listeners[i],
                scope = listener.customScope || this,
                data = [].slice.call(arguments, 1);

            listenerReturn = listener.apply(scope, data);
            if (listenerReturn === false)
                eventReturn = false;
        }

        return eventReturn;
    };
};

/**
 * UI functions
 */
WR.ui = {};

WR.ui.overlay = {
    options: {
        css: {
            zIndex: 1000,
            background: '#000',
            opacity: .5
        },
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
    },

    overlay: null,
    container: "body",

    methods: {
        fadeIn: function(overlay) {
            overlay.fadeIn(500);
        },

        show: function(overlay) {
            overlay.show();
        },

        fadeOut: function(overlay) {
            overlay.fadeOut(300);
        },

        hide: function(overlay) {
            overlay.hide();
        }
    },

    init: function() {
        if (!window.jQuery)
            return;

        $('head').append([
            '<style type="text/css">',
            '.overlay { width: 100%; min-height: 100%; position: fixed; top: 0; left: 0; display: none; }',
            '* html .overlay { height: 100%; position: absolute; }',
            '</style>'
        ].join(''));

        this.overlay = $('<div class="overlay"></div>');
        this.overlay.appendTo(this.container);

        // Hide overlay on some events
        var self = this;
        $(window).bind('keypress', function(e) {
            if (e.keyCode == 27)
                self.hide();
        });
        this.overlay.click($.proxy(this, 'hide'));

        this.updateStyles();
    },

    bind: function() {
        if (!window.jQuery)
            return;

        if (!this.overlay)
            this.init();

        return this.overlay.bind.apply(this.overlay, arguments);
    },

    unbind: function() {
        if (!window.jQuery)
            return;

        if (!this.overlay)
            this.init();

        return this.overlay.unbind.apply(this.overlay, arguments);
    },

    updateStyles: function(newStyles) {
        $.extend(this.options.css, newStyles);
        this.overlay.css(this.options.css);
    },

    show: function() {
        if (!window.jQuery)
            return;

        if (!this.overlay)
            this.init();

        this.beforeShow();

        this.methods[this.options.showMethod](this.overlay);
    },

    beforeShow: function() {
        this.overlay.height($(this.container).height());
    },

    hide: function() {
        if (!window.jQuery)
            return;

        if (!this.overlay)
            this.init();

        this.methods[this.options.hideMethod](this.overlay);

        this.overlay.trigger('hide', this);
    }
};

WR.ui.position = {
    /**
     * Get window scroll left and top
     */
    getScrollXY: function() {
        var scrOfX = 0, scrOfY = 0;
        if (typeof(window.pageYOffset) == 'number') {
            //Netscape compliant
            scrOfY = window.pageYOffset;
            scrOfX = window.pageXOffset;
        } else if (document.body && (document.body.scrollLeft || document.body.scrollTop)) {
            //DOM compliant
            scrOfY = document.body.scrollTop;
            scrOfX = document.body.scrollLeft;
        } else if (document.documentElement && (document.documentElement.scrollLeft || document.documentElement.scrollTop)) {
            //IE6 standards compliant mode
            scrOfY = document.documentElement.scrollTop;
            scrOfX = document.documentElement.scrollLeft;
        }
        return {x: scrOfX, y: scrOfY};
    }
};

/**
 * Data-related stuff:
 * set, array, object, other data-structures and related methods
 */
WR.data = {};

/**
 * Collection
 * Something between Array and Object :)
 * @param {Array} items
 * @constructor
 */
WR.data.Collection = function(items) {
    this.items = [];

    if (items instanceof WR.data.Collection)
        items = items.toArray();

    if ($.isArray(items))
        this.proxyFn('push', items);
};

WR.data.Collection.prototype = {
    // @private
    items: null,

    getLength: function() {
        return this.items.length;
    },

    proxyFn: function(fnName, args) {
        return this.items[fnName].apply(this.items, args);
    },

    /**
     * Proxy for [].push(new1, [new2, new3, ...])
     * Adds one ore more elements to the end of the array
     * @return {Number} new array length
     */
    push: function() {
        return this.proxyFn('push', arguments);
    },

    /**
     * Proxy for [].pop()
     * Removes the last element of the array
     * @return removed element
     */
    pop: function() {
        return this.proxyFn('pop', arguments);
    },

    /**
     * Proxy for [].shift()
     * Removes the first element of the array
     * @return removed element
     */
    shift: function() {
        return this.proxyFn('shift', arguments);
    },

    /**
     * Proxy for [].unshift(new1, [new2, new3, ...])
     * Adds one ore more elements to the beginning of the array
     * @return {Number} new array length
     */
    unshift: function() {
        return this.proxyFn('unshift', arguments);
    },

    /**
     * Proxy for [].slice(fromPos, [toPos])
     * @return {WebRiders.data.Collection} sliced sub-collection (from fromPos index till toPos index)
     */
    slice: function() {
        this.proxyFn('slice', arguments);
        return this;
    },

    /**
     * Proxy for [].splice(fromPos, [howMany, [new1, [new2, new3, ...]]])
     * Removes howMany elements from fromPos index and inserts there one or more new elements
     * @return {WebRiders.data.Collection} spliced sub-collection
     */
    splice: function() {
        this.proxyFn('splice', arguments);
        return this;
    },

    /**
     * Get item by id
     * @param id
     * @return found element or undefined
     */
    getById: function(id) {
        return this.get({ 'id': id })[0];
    },

    /**
     * Get item by something
     *
     * @param {String/Number/Function/Object} by:
     *     0, 1, 2, 'asd', 'qwe' - returns array item by index (or smth)
     *     { year: 2009, sum: 15 } - returns array items, that has EXACTLY the same params (year === 2009, sum === 15)
     *     { x: null, y: undefined } - true, when item.x === null and item.x in not defined
     *     { z: '*' } - spacial case. Equal to any (you can't use '*' as just '*', sorry).
     *     function(o) { return o.year === 2009 && sum === 15; } - filter by function
     *
     * @return {Array} found elements (may be empty but still Array)
     */
    get: function(by) {
        // Filter by params set
        if (typeof by == "object") {
            var ret = [];

            function _cmp(o1, o2) {
                for (var k in o1) {
                    if (o1.hasOwnProperty(k)) {
                        if (o1[k] === '*' && o2.hasOwnProperty(k))
                            continue;

                        if (o1[k] !== o2[k])
                            return false;
                    }

                }
                return true;
            }

            for (var i = 0, it = this.items, l = it.length; i < l; i++)
                if (_cmp(by, it[i]))
                    ret.push(it[i]);

            return ret;
        }
        // Filter by function
        else if (typeof by == "function") {
            var ret = [];

            for (var i = 0, it = this.items, l = it.length; i < l; i++)
                if (by.call(it[i], it[i]))
                    ret.push(it[i]);

            return ret;
        }
        // Get by index
        else {
            return this.items[by];
        }
    },

    /**
     * Items iterator
     * @param {Function/String} fn - function or method name
     */
    each: function(fn) {
        if (typeof fn == "function")
            return $.each(this.items, fn);
        else if (typeof fn == "string")
            return $.each(this.items, function() {
                this[fn]();
            });
    },

    toArray: function() {
        return this.items;
    },

    toString: function() {
        return this.items.toString();
    }
};

/**
 * Alias for WR.data.Collection
 */
WR.data.C = WR.data.Collection;