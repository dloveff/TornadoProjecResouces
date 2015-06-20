/**
 * Created by chinfeng on 14-1-16.
 */

function __create_node(doc, tag, value) {
    var elm = doc.createElement(tag);
    elm.appendChild(doc.createCDATASection(value));
    return elm;
}

function __append_cdata_node(doc, parent, tag, value) {
    var elm = doc.createElement(tag);
    elm.appendChild(doc.createCDATASection(value));
    parent.appendChild(elm);
    return elm;
}

function service_to_form(url, type, frm) {
    $.ajax({
        type: type,
        url: url,
        success: function(response, status, jqXHR) {
            xml_to_form(response, frm);
        },
        error: function(jqXHR, status, error) { /* ... */ }
    });
}


function get_service(url) {
    var rt;
    $.ajax({
        type: 'GET',
        url: url,
        async: false,
        success: function(response, status, jqXHR) {
            rt = response;
        },
        error: function(jqXHR, status, error) { /* ... */ }
    });

    return rt;
}

function binding_service(elm, surl)  {
    $.ajax({
        type: 'GET',
        url: surl,
        dataType: 'xml',
        success: function(doc, status, jqXHR) {
            $(doc).xpath('yy');
        },
        error: function(jqXHR, status, error) { /* ... */ }
    });
}


function xml_to_form(xml, frm) {
    $(':eq(0)', xml).each(function () {
        $.each(this.attributes, function () {
            if(this.specified) {
                var name = this.name;
                var value = this.value;
                $('[name="' + name + '"]', frm).each(function() {
                    if ($(this).prop('tagName') == 'A') {
                        var prefix = $(this).attr('data-link-prefix');
                        $(this).attr('href', prefix + value);
                    } else if ($(this).prop('tagName') == 'INPUT') {
                        $(this).val(value);
                    } else {
                        $(this).text(value);
                    }
                });
            }
        });
    });
    $(':eq(0)', xml).children().each(function () {
        var name = $(this).prop('tagName');
        var value = $(this).text();
        $('[name="' + name + '"]', frm).each(function() {
            if ($(this).prop('tagName') == 'A') {
                var prefix = $(this).attr('data-link-prefix');
                $(this).attr('href', prefix + value);
            } else if ($(this).prop('tagName') == 'INPUT') {
                $(this).val(value);
            } else {
                $(this).text(value);
            }
        });
    });

    var after_callback_func = $(frm).attr('data-after-callback');
    if ((after_callback_func != undefined) && (after_callback_func in window)) {
        window[after_callback_func](frm);
    }
}

function form_to_xml(frm) {
    var doc = $.parseXML('<' + $(frm).attr('name') + '/>');
    $('[name]:input', frm).each(function() {
        __append_cdata_node(doc, doc.documentElement, $(this).attr('name'), $(this).val());
    });
    return (new XMLSerializer().serializeToString(doc));
}

function form_to_service(elm, success, error) {
    var $frm = $(elm).closest('form');
    var url = $frm.attr('action');
    var type = $frm.attr('method');
    var data = form_to_xml($frm);
    $.ajax({
        url: url,
        type: type,
        data: data,
        success: success,
        error: error
    });
}

function service_iter_to_form(url, type, frm, iter) {
    $.ajax({
        type: type,
        url: url,
        success: function(response, status, jqXHR) {
            xml_iter_to_form(response, frm, iter);

            var after_callback_func = $(frm).attr('data-after-callback');
            if ((after_callback_func != undefined) && (after_callback_func in window)) {
                window[after_callback_func](frm);
            }
        },
        error: function(jqXHR, status, error) { /* ... */ }
    });
}

function xml_iter_to_form(xml, frm, iter) {
    var iter_elm_o = $('[name="' + iter + '"]:first', frm).detach();
    $(frm).remove('[name="' + iter + '"]');

    var items = [];
    $(':first', xml).children().each(function () {
        var iter_elm = iter_elm_o.clone();
        $.each(this.attributes, function () {
            if(this.specified) {
                var name = this.name;
                var value = this.value;
                $('[name="' + name + '"]', iter_elm).each(function() {
                    if ($(this).prop('tagName') == 'A') {
                        var prefix = $(this).attr('data-link-prefix');
                        $(this).attr('href', prefix + value);
                    } else if ($(this).prop('tagName') == 'INPUT') {
                        $(this).val(value);
                    } else {
                        $(this).text(value);
                    }
                });
            }
        });

        $(this).children().each(function () {
            var name = $(this).prop('tagName');
            var value = $(this).text();
            $('[name="' + name + '"]', iter_elm).each(function() {
                if ($(this).prop('tagName') == 'A') {
                    var prefix = $(this).attr('data-link-prefix');
                    $(this).attr('href', prefix + value);
                } else if ($(this).prop('tagName') == 'INPUT') {
                    $(this).val(value);
                } else {
                    $(this).text(value);
                }
            });
        });

        items.push(iter_elm);
    });

    $(frm).empty();
    $(frm).append(items);
}

function load_service(elm) {
    var url = $(elm).attr('data-service-url');
    var type = $(elm).attr('data-service-type');
    var iter = $(elm).attr('data-iter-name');
    if (iter == undefined) {
        /* 单个数据项目 */
        service_to_form(url, type, elm);
    } else {
        /* 多个数据项目 */
        service_iter_to_form(url, type, elm, iter);
    }

}

(function($) {
    $(document).ready(function() {
        $('[data-service-url]').each(function () {
            load_service(this);
        });
    })
}(jQuery));

