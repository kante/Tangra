window.undefined = window.undefined;

function jQuery(a, c) {
    this.cur = $.Select(a || $.context || document, c && c.$jquery && c.get(0) || c)
}
if (window.$ == undefined) var $ = function (a, c) {
    return new jQuery(a, c)
};
jQuery.prototype = $.fn = {
    $jquery: "$Rev: 100 $",
    size: function () {
        return this.get().length
    },
    get: function (i) {
        return i == undefined ? this.cur : this.cur[i]
    },
    each: function (f) {
        for (var i = 0; i < this.size(); i++) f.apply(this.get(i), [i]);
        return this
    },
    set: function (a, b) {
        return this.each(function () {
            if (b == undefined)
                for (var j in a) $.attr(this, j, a[j]);
            else $.attr(this, a, b)
        })
    },
    html: function (h) {
        return h == undefined && this.size() ? this.get(0).innerHTML : this.set("innerHTML", h)
    },
    val: function (h) {
        return h == undefined && this.size() ? this.get(0).value : this.set("value", h)
    },
    text: function (e) {
        e = e || this.get();
        var t = "";
        for (var j = 0; j < e.length; j++)
            for (var i = 0; i < e[j].childNodes.length; i++) t += e[j].childNodes[i].nodeType != 1 ? e[j].childNodes[i].nodeValue : $.fn.text(e[j].childNodes[i].childNodes);
        return t
    },
    css: function (a, b) {
        return a.constructor != String || b ? this.each(function () {
            if (!b)
                for (var j in a) $.attr(this.style, j, a[j]);
            else $.attr(this.style, a, b)
        }) : $.css(this.get(0), a)
    },
    toggle: function () {
        return this.each(function () {
            var d = $.css(this, "display");
            if (d == "none" || d === "") $(this).show();
            else $(this).hide()
        })
    },
    show: function () {
        return this.each(function () {
            this.style.display = this.oldblock ? this.oldblock : "";
            if ($.css(this, "display") == "none") this.style.display = "block"
        })
    },
    hide: function () {
        return this.each(function () {
            this.oldblock = $.css(this, "display");
            if (this.oldblock == "none") this.oldblock = "block";
            this.style.display = "none"
        })
    },
    addClass: function (c) {
        return this.each(function () {
            $.$class.add(this, c)
        })
    },
    removeClass: function (c) {
        return this.each(function () {
            $.$class.remove(this, c)
        })
    },
    toggleClass: function (c) {
        return this.each(function () {
            if ($.hasWord(this, c)) $.$class.remove(this, c);
            else $.$class.add(this, c)
        })
    },
    remove: function () {
        this.each(function () {
            this.parentNode.removeChild(this)
        });
        this.cur = [];
        return this
    },
    wrap: function () {
        var a = $.clean(arguments);
        return this.each(function () {
            var b = a[0].cloneNode(true);
            this.parentNode.insertBefore(b, this);
            while (b.firstChild) b = b.firstChild;
            b.appendChild(this)
        })
    },
    append: function () {
        var clone = this.size() > 1;
        var a = $.clean(arguments);
        return this.domManip(function () {
            for (var i = 0; i < a.length; i++) this.appendChild(clone ? a[i].cloneNode(true) : a[i])
        })
    },
    appendTo: function () {
        var a = arguments;
        return this.each(function () {
            for (var i = 0; i < a.length; i++) $(a[i]).append(this)
        })
    },
    prepend: function () {
        var clone = this.size() > 1;
        var a = $.clean(arguments);
        return this.domManip(function () {
            for (var i = a.length - 1; i >= 0; i--) this.insertBefore(clone ? a[i].cloneNode(true) : a[i], this.firstChild)
        })
    },
    before: function () {
        var clone = this.size() > 1;
        var a = $.clean(arguments);
        return this.each(function () {
            for (var i = 0; i < a.length; i++) this.parentNode.insertBefore(clone ? a[i].cloneNode(true) : a[i], this)
        })
    },
    after: function () {
        var clone = this.size() > 1;
        var a = $.clean(arguments);
        return this.each(function () {
            for (var i = a.length - 1; i >= 0; i--) this.parentNode.insertBefore(clone ? a[i].cloneNode(true) : a[i], this.nextSibling)
        })
    },
    empty: function () {
        return this.each(function () {
            while (this.firstChild) this.removeChild(this.firstChild)
        })
    },
    bind: function (t, f) {
        return this.each(function () {
            $.event.add(this, t, f)
        })
    },
    unbind: function (t, f) {
        return this.each(function () {
            $.event.remove(this, t, f)
        })
    },
    trigger: function (t) {
        return this.each(function () {
            $.event.trigger(this, t)
        })
    },
    find: function (t) {
        var old = [],
            ret = [];
        this.each(function () {
            old[old.length] = this;
            ret = $.merge(ret, $.Select(t, this))
        });
        this.old = old;
        this.cur = ret;
        return this
    },
    end: function () {
        this.cur = this.old;
        return this
    },
    parent: function (a) {
        this.cur = $.map(this.cur, "d.parentNode");
        if (a) this.cur = $.filter(a, this.cur).r;
        return this
    },
    parents: function (a) {
        this.cur = $.map(this.cur, $.parents);
        if (a) this.cur = $.filter(a, this.cur).r;
        return this
    },
    siblings: function (a) {
        this.cur = $.map(this.cur, $.sibling);
        if (a) this.cur = $.filter(a, this.cur).r;
        return this
    },
    filter: function (t) {
        this.cur = $.filter(t, this.cur).r;
        return this
    },
    not: function (t) {
        this.cur = t.constructor == String ? $.filter(t, this.cur, false).r : $.grep(this.cur, function (a) {
            return a != t
        });
        return this
    },
    add: function (t) {
        this.cur = $.merge(this.cur, t.constructor == String ? $.Select(t) : t.constructor == Array ? t : [t]);
        return this
    },
    is: function (t) {
        return $.filter(t, this.cur).r.length > 0
    },
    domManip: function (fn) {
        return this.each(function () {
            var obj = this;
            if (this.nodeName == "TABLE") {
                var tbody = this.getElementsByTagName("tbody");
                if (!tbody.length) {
                    obj = document.createElement("tbody");
                    this.appendChild(obj)
                } else obj = tbody[0]
            }
            fn.apply(obj)
        })
    }
};
$.$class = {
    add: function (o, c) {
        if ($.hasWord(o, c)) return;
        o.className += (o.className.length > 0 ? " " : "") + c
    },
    remove: function (o, c) {
        o.className = !c ? "" : o.className.replace(new RegExp("(^|\\s*\\b[^-])" + c + "($|\\b(?=[^-]))", "g"), "")
    }
};
(function () {
    var b = navigator.userAgent.toLowerCase();
    $.browser = (/webkit/.test(b) && "safari") || (/opera/.test(b) && "opera") || (/msie/.test(b) && "msie") || (!/compatible/.test(b) && "mozilla") || "other";
    $.boxModel = ($.browser != "msie" || document.compatMode == "CSS1Compat")
})();
$.css = function (e, p) {
    if (p == "height" || p == "width") {
        var ph = (!$.boxModel ? 0 : $.css(e, "paddingTop") + $.css(e, "paddingBottom") + $.css(e, "borderTopWidth") + $.css(e, "borderBottomWidth")) || 0;
        var pw = (!$.boxModel ? 0 : $.css(e, "paddingLeft") + $.css(e, "paddingRight") + $.css(e, "borderLeftWidth") + $.css(e, "borderRightWidth")) || 0;
        var oHeight, oWidth;
        if ($.css(e, "display") != 'none') {
            oHeight = e.offsetHeight || parseInt(e.style.height) || 0;
            oWidth = e.offsetWidth || parseInt(e.style.width) || 0
        } else {
            var els = e.style;
            var ov = els.visibility;
            var op = els.position;
            var od = els.display;
            els.visibility = "hidden";
            els.position = "absolute";
            els.display = "";
            oHeight = e.clientHeight || parseInt(e.style.height);
            oWidth = e.clientWidth || parseInt(e.style.width);
            els.display = od;
            els.position = op;
            els.visibility = ov
        }
        return p == "height" ? (oHeight - ph < 0 ? 0 : oHeight - ph) : (oWidth - pw < 0 ? 0 : oWidth - pw)
    }
    var r;
    if (e.style[p]) r = e.style[p];
    else if (e.currentStyle) r = e.currentStyle[p];
    else if (document.defaultView && document.defaultView.getComputedStyle) {
        p = p.replace(/([A-Z])/g, "-$1").toLowerCase();
        var s = document.defaultView.getComputedStyle(e, "");
        r = s ? s.getPropertyValue(p) : null
    }
    return /top|right|left|bottom/i.test(p) ? parseFloat(r) : r
};
$.clean = function (a) {
    var r = [];
    for (var i = 0; i < a.length; i++) {
        if (a[i].constructor == String) {
            if (!a[i].indexOf("<tr")) {
                var tr = true;
                a[i] = "<table>" + a[i] + "</table>"
            } else if (!a[i].indexOf("<td") || !a[i].indexOf("<th")) {
                var td = true;
                a[i] = "<table><tbody><tr>" + a[i] + "</tr></tbody></table>"
            }
            var div = document.createElement("div");
            div.innerHTML = a[i];
            if (tr || td) {
                div = div.firstChild.firstChild;
                if (td) div = div.firstChild
            }
            for (var j = 0; j < div.childNodes.length; j++) r[r.length] = div.childNodes[j]
        } else if (a[i].length && !a[i].nodeType)
            for (var k = 0; k < a[i].length; k++) r[r.length] = a[i][k];
        else if (a[i] !== null) r[r.length] = a[i].nodeType ? a[i] : document.createTextNode(a[i].toString())
    }
    return r
};
$.g = {
    "": "m[2]== '*'||a.nodeName.toUpperCase()==m[2].toUpperCase()",
    "#": "a.getAttribute('id')&&a.getAttribute('id')==m[2]",
    ":": {
        lt: "i<m[3]-0",
        gt: "i>m[3]-0",
        nth: "m[3]-0==i",
        eq: "m[3]-0==i",
        first: "i==0",
        last: "i==r.length-1",
        even: "i%2==0",
        odd: "i%2==1",
        "first-child": "$.sibling(a,0).cur",
        "nth-child": "(m[3]=='even'?$.sibling(a,m[3]).n%2==0:(m[3]=='odd'?$.sibling(a,m[3]).n%2==1:$.sibling(a,m[3]).cur))",
        "last-child": "$.sibling(a,0,true).cur",
        "nth-last-child": "$.sibling(a,m[3],true).cur",
        "first-of-type": "$.ofType(a,0)",
        "nth-of-type": "$.ofType(a,m[3])",
        "last-of-type": "$.ofType(a,0,true)",
        "nth-last-of-type": "$.ofType(a,m[3],true)",
        "only-of-type": "$.ofType(a)==1",
        "only-child": "$.sibling(a).length==1",
        parent: "a.childNodes.length",
        empty: "!a.childNodes.length",
        root: "a==(a.ownerDocument||document).documentElement",
        contains: "(a.innerText||a.innerHTML).indexOf(m[3])!=-1",
        visible: "(!a.type||a.type!='hidden')&&($.css(a,'display')!= 'none'&&$.css(a,'visibility')!= 'hidden')",
        hidden: "(a.type&&a.type == 'hidden')||$.css(a,'display')=='none'||$.css(a,'visibility')== 'hidden'",
        enabled: "a.disabled==false",
        disabled: "a.disabled",
        checked: "a.checked"
    },
    ".": "$.hasWord(a,m[2])",
    "@": {
        "=": "$.attr(a,m[3])==m[4]",
        "!=": "$.attr(a,m[3])!=m[4]",
        "~=": "$.hasWord($.attr(a,m[3]),m[4])",
        "|=": "!$.attr(a,m[3]).indexOf(m[4])",
        "^=": "!$.attr(a,m[3]).indexOf(m[4])",
        "$=": "$.attr(a,m[3]).substr( $.attr(a,m[3]).length - m[4].length,m[4].length )==m[4]",
        "*=": "$.attr(a,m[3]).indexOf(m[4])>=0",
        "": "m[3]=='*'?a.attributes.length>0:$.attr(a,m[3])"
    },
    "[": "$.Select(m[2],a).length"
};
$.token = ["\\.\\.|/\\.\\.", "a.parentNode", ">|/", "$.sibling(a.firstChild)", "\\+", "$.sibling(a).next", "~",
    function (a) {
        var r = [];
        var s = $.sibling(a);
        if (s.n > 0)
            for (var i = s.n; i < s.length; i++) r[r.length] = s[i];
        return r
    }
];
$.Select = function (t, context) {
    context = context || $.context || document;
    if (t.constructor != String) return [t];
    if (!t.indexOf("//")) {
        context = context.documentElement;
        t = t.substr(2, t.length)
    } else if (!t.indexOf("/")) {
        context = context.documentElement;
        t = t.substr(1, t.length);
        if (t.indexOf("/") >= 1) t = t.substr(t.indexOf("/"), t.length)
    }
    var ret = [context];
    var done = [];
    var last = null;
    while (t.length > 0 && last != t) {
        var r = [];
        last = t;
        t = $.cleanSpaces(t).replace(/^\/\//i, "");
        var foundToken = false;
        for (var i = 0; i < $.token.length; i += 2) {
            var re = new RegExp("^(" + $.token[i] + ")");
            var m = re.exec(t);
            if (m) {
                r = ret = $.map(ret, $.token[i + 1]);
                t = $.cleanSpaces(t.replace(re, ""));
                foundToken = true
            }
        }
        if (!foundToken) {
            if (!t.indexOf(",") || !t.indexOf("|")) {
                if (ret[0] == context) ret.shift();
                done = $.merge(done, ret);
                r = ret = [context];
                t = " " + t.substr(1, t.length)
            } else {
                var re2 = /^([#.]?)([a-z0-9\\*_-]*)/i;
                var m = re2.exec(t);
                if (m[1] == "#") {
                    var oid = document.getElementById(m[2]);
                    r = ret = oid ? [oid] : [];
                    t = t.replace(re2, "")
                } else {
                    if (!m[2] || m[1] == ".") m[2] = "*";
                    for (var i = 0; i < ret.length; i++) r = $.merge(r, $.tag(ret[i], m[2]))
                }
            }
        }
        if (t) {
            var val = $.filter(t, r);
            ret = r = val.r;
            t = $.cleanSpaces(val.t)
        }
    }
    if (ret && ret[0] == context) ret.shift();
    done = $.merge(done, ret);
    return done
};
$.tag = function (a, b) {
    return a && a.getElementsByTagName != undefined ? a.getElementsByTagName(b) : []
};
$.attr = function (o, a, v) {
    if (a && a.constructor == String) {
        var fix = {
            "for": "htmlFor",
            "class": "className",
            "float": "cssFloat"
        };
        a = (fix[a] && fix[a].replace && fix[a]) || a;
        var r = /-([a-z])/ig;
        a = a.replace(r, function (z, b) {
            return b.toUpperCase()
        });
        if (v != undefined) {
            o[a] = v;
            if (o.setAttribute && a != "disabled") o.setAttribute(a, v)
        }
        return o[a] || o.getAttribute(a) || ""
    } else return ""
};
$.filter = function (t, r, not) {
    var g = $.grep;
    if (not === false) g = function (a, f) {
        return $.grep(a, f, true)
    };
    while (t && t.match(/^[:\\.#\\[a-zA-Z\\*]/)) {
        var re = /^\[ *@([a-z0-9*()_-]+) *([~!|*$^=]*) *'?"?([^'"]*)'?"? *\]/i;
        var m = re.exec(t);
        if (m) m = ["", "@", m[2], m[1], m[3]];
        else {
            re = /^(\[) *([^\]]*) *\]/i;
            m = re.exec(t);
            if (!m) {
                re = /^(:)([a-z0-9*_-]*)\( *["']?([^ \)'"]*)['"]? *\)/i;
                m = re.exec(t);
                if (!m) {
                    re = /^([:\.#]*)([a-z0-9*_-]*)/i;
                    m = re.exec(t)
                }
            }
        }
        t = t.replace(re, "");
        if (m[1] == ":" && m[2] == "not") r = $.filter(m[3], r, false).r;
        else {
            var f = null;
            if ($.g[m[1]].constructor == String) f = $.g[m[1]];
            else if ($.g[m[1]][m[2]]) f = $.g[m[1]][m[2]];
            if (f) {
                eval("f = function(a,i){return " + f + "}");
                r = g(r, f)
            }
        }
    }
    return {
        r: r,
        t: t
    }
};
$.parents = function (a) {
    var b = [];
    var c = a.parentNode;
    while (c && c != document) {
        b[b.length] = c;
        c = c.parentNode
    }
    return b
};
$.cleanSpaces = function (t) {
    return t.replace(/^\s+|\s+$/g, "")
};
$.ofType = function (a, n, e) {
    var t = $.grep($.sibling(a), function (b) {
        return b.nodeName == a.nodeName
    });
    if (e) n = t.length - n - 1;
    return n != undefined ? t[n] == a : t.length
};
$.sibling = function (a, n, e) {
    var type = [];
    var tmp = a.parentNode.childNodes;
    for (var i = 0; i < tmp.length; i++) {
        if (tmp[i].nodeType == 1) type[type.length] = tmp[i];
        if (tmp[i] == a) type.n = type.length - 1
    }
    if (e) n = type.length - n - 1;
    type.cur = (type[n] == a);
    type.prev = (type.n > 0 ? type[type.n - 1] : null);
    type.next = (type.n < type.length - 1 ? type[type.n + 1] : null);
    return type
};
$.hasWord = function (e, a) {
    if (e == undefined) return;
    if (e.className) e = e.className;
    return new RegExp("(^|\\s)" + a + "(\\s|$)").test(e)
};
$.getAll = function (o, r) {
    r = r || [];
    var s = o.childNodes;
    for (var i = 0; i < s.length; i++)
        if (s[i].nodeType == 1) {
            r[r.length] = s[i];
            $.getAll(s[i], r)
        }
    return r
};
$.merge = function (a, b) {
    var d = [];
    for (var k = 0; k < b.length; k++) d[k] = b[k];
    for (var i = 0; i < a.length; i++) {
        var c = true;
        for (var j = 0; j < b.length; j++)
            if (a[i] == b[j]) c = false;
        if (c) d[d.length] = a[i]
    }
    return d
};
$.grep = function (a, f, s) {
    if (f.constructor == String) f = new Function("a", "i", "return " + f);
    var r = [];
    if (a != undefined)
        for (var i = 0; i < a.length; i++)
            if ((!s && f(a[i], i)) || (s && !f(a[i], i))) r[r.length] = a[i];
    return r
};
$.map = function (a, f) {
    if (f.constructor == String) f = new Function("a", "return " + f);
    var r = [];
    for (var i = 0; i < a.length; i++) {
        var t = f(a[i], i);
        if (t !== null) {
            if (t.constructor != Array) t = [t];
            r = $.merge(t, r)
        }
    }
    return r
};
$.event = {};
$.event.add = function (element, type, handler) {
    if ($.browser == "msie" && element.setInterval != undefined) element = window;
    if (!handler.$$guid) handler.$$guid = $.event.add.guid++;
    if (!element.events) element.events = {};
    var handlers = element.events[type];
    if (!handlers) {
        handlers = element.events[type] = {};
        if (element["on" + type]) handlers[0] = element["on" + type]
    }
    handlers[handler.$$guid] = handler;
    element["on" + type] = $.event.handle
};
$.event.add.guid = 1;
$.event.remove = function (element, type, handler) {
    if (element.events)
        if (type && element.events[type])
            if (handler) delete element.events[type][handler.$$guid];
            else
                for (var i in element.events[type]) delete element.events[type][i];
            else
                for (var j in element.events) $.event.remove(element, j)
};
$.event.trigger = function (element, type, data) {
    data = data || [$.event.fix({
        type: type
    })];
    if (element && element["on" + type]) element["on" + type].apply(element, data)
};
$.event.handle = function (event) {
    if (!event && !window.event) return;
    var returnValue = true,
        handlers = [];
    event = event || $.event.fix(window.event);
    for (var j in this.events[event.type]) handlers[handlers.length] = this.events[event.type][j];
    for (var i = 0; i < handlers.length; i++) {
        if (handlers[i].constructor == Function) {
            this.$$handleEvent = handlers[i];
            if (this.$$handleEvent(event) === false) {
                event.preventDefault();
                event.stopPropagation();
                returnValue = false
            }
        }
    }
    return returnValue
};
$.event.fix = function (event) {
    event.preventDefault = $.event.fix.preventDefault;
    event.stopPropagation = $.event.fix.stopPropagation;
    return event
};
$.event.fix.preventDefault = function () {
    this.returnValue = false
};
$.event.fix.stopPropagation = function () {
    this.cancelBubble = true
};
$.fn._toggle = $.fn.toggle;
$.fn.toggle = function (a, b) {
    return a && b ? this.click(function (e) {
        this.last = this.last == a ? b : a;
        e.preventDefault();
        return $.apply(this, this.last, [e]) || false
    }) : this._toggle()
};
$.fn.hover = function (f, g) {
    function handleHover(e) {
        var p = e.fromElement || e.toElement || e.relatedTarget;
        while (p && p != this) p = p.parentNode;
        if (p == this) return false;
        return (e.type == "mouseover" ? f : g).apply(this, [e])
    }
    return this.mouseover(handleHover).mouseout(handleHover)
};
$.fn.ready = function (f) {
    if ($.isReady) $.apply(document, f);
    else {
        $.readyList.push(f)
    }
    return this
};
(function () {
    var e = ["blur", "focus", "contextmenu", "load", "resize", "scroll", "unload", "click", "dblclick", "mousedown", "mouseup", "mouseenter", "mouseleave", "mousemove", "mouseover", "mouseout", "change", "reset", "select", "submit", "keydown", "keypress", "keyup", "abort", "error", "ready"];
    for (var i = 0; i < e.length; i++) {
        (function () {
            var o = e[i];
            $.fn[o] = function (f) {
                return this.bind(o, f)
            };
            $.fn["un" + o] = function (f) {
                return this.unbind(o, f)
            };
            $.fn["do" + o] = function () {
                return this.trigger(o)
            };
            $.fn["one" + o] = function (f) {
                return this.bind(o, function (e) {
                    if (this[o + f] !== null) return true;
                    this[o + f]++;
                    return $.apply(this, f, [e])
                })
            }
        })()
    }
    $.isReady = false;
    $.readyList = [];
    $.ready = function () {
        if (!$.isReady) {
            $.isReady = true;
            if ($.readyList) {
                for (var i = 0; i < $.readyList.length; i++) $.apply(document, $.readyList[i]);
                $.readyList = null
            }
        }
    };
    if ($.browser == "mozilla" || $.browser == "opera") {
        $.event.add(document, "DOMContentLoaded", $.ready)
    } else if ($.browser == "msie") {
        document.write("<scr" + "ipt id=__ie_init defer=true " + "src=javascript:void(0)><\/script>");
        var script = document.getElementById("__ie_init");
        script.onreadystatechange = function () {
            if (this.readyState == "complete") $.ready()
        };
        script = null
    } else if ($.browser == "safari") {
        $.safariTimer = setInterval(function () {
            if (document.readyState == "loaded" || document.readyState == "complete") {
                clearInterval($.safariTimer);
                $.safariTimer = null;
                $.ready()
            }
        }, 10)
    }
    $.event.add(window, "load", $.ready)
})();