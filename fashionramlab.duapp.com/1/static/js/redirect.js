/**
 * Created by chinfeng on 13-12-31.
 */
(function(window,$){
    var storage = window.localStorage;

    var getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]); return null;
    };

    var redirect = function(url){
        //芝麻开门实现，另外逻辑在weiba.js
        if(!url){
            url = storage.getItem('weiba.history');
            if(!url){
                url = '/';
            }
        }

        url = decodeURIComponent(url);

        if(window.history.replaceState){
            var new_url = url.replace('http://','').toLowerCase();
            if(new_url.indexOf(location.host)==0){
                window.history.replaceState({},'',url);
            }
        }
        window.location.replace(url);
    };

    redirect(getUrlParam('redirect'));

})(window,jQuery);