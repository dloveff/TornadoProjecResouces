(function($) {
    $(document).ready(function() {
        $('[data-dialog-options]').each(function () {
            var options_var_name = $(this).attr('data-dialog-options');
            if (options_var_name in window) {
                var opt = window[options_var_name];
                opt.autoOpen = false;
                opt.closeOnEscape = true;
                opt.hide = { effect: 'blind', duration: 500 }
                opt.show = { effect: 'blind', duration: 500 }
                opt.width = 860;
                opt.height = $(window).height() * 0.8;
                //opt.draggable = false;
                $(this).addClass('ui-widget ui-widget-content ui-corner-all');
                $(this).dialog(opt);
                $('[data-dialog-for="' + $(this).attr('id') + '"]').bind('click', function() {
                    var dialog_id = $(this).attr('data-dialog-for');
                    $('#' + dialog_id).dialog('open');
                });
                
            }
        });

        $('[data-frame-dialog]').on('click', function (event) {
            event.preventDefault();
            var url = $(this).attr('data-frame-dialog');
            var title = $(this).attr('title');
            $('<div id="frame-dialog" style="overflow:hidden;margin:0;padding:0"><iframe frameborder="0" style="width:100%;height:100%" src="' + url + '" /></div>').dialog({
                autoOpen: true,
                modal: true,
                autoResize: false,
                title: title,
                height: 600,
                width: 800  ,
                autoResize: true,
                overlay: {
                    opacity: 0.5,
                    background: 'black'
                },
                open: function(event, ui) {
                    $('iframe', this).load(function () {
                        $(this).contents().find('button[data-dialog-button]').on('click', function() {
                            var func = $(this).attr('data-dialog-button');
                            if (func == 'close') {
                                window.parent.jQuery('iframe').closest('div').dialog('close');
                            }
                        });
                    });
                },
                close: function( event, ui ) {
                    $(this).dialog('destroy').remove()
                },
                resizeStart: function(event, ui) {
                    var $dialog = $(this).closest('.ui-dialog');
                    var $div = $('<div id="_iframe_p_" style="background-color:red;position:absolute;width:100%;height:100%;z-index:9999999"></div>')  
                    $div.fadeTo(0);   
                    $div.appendTo($dialog);
                    $div.css('left', 0);  
                    $div.css('top', 0);
                },
                resizeStop: function(event, ui) {
                    $(':parent #_iframe_p_').remove();  
                }
            });
        });
    });
    
}(jQuery));