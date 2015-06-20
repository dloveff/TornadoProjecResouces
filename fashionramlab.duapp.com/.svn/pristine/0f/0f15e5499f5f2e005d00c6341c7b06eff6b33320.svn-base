/**
 * Created by 锦峰 on 14-1-10.
 */
var map = null;
var driving = null;
var walking = null;

function init_map(holder_id) {
    map = new BMap.Map(holder_id);
    var x1=getQueryString("x");
    var y1=getQueryString("y");
	var point = new BMap.Point(x1, y1);
	map.centerAndZoom(point,14);
	map.enableScrollWheelZoom();
    driving = new BMap.DrivingRoute(map, {
	 renderOptions: {
	   map: map,
	   autoViewport: true
	 }
	});
    walking = new BMap.WalkingRoute(map, {
	 renderOptions: {
	   map: map,
	   autoViewport: true
	 }
	});
    drive_route(113.112656,23.029751);
}

function drive_route(x, y) {
    search_route(driving, x, y);
}

function walk_route(x, y) {
    search_route(walking, x, y);
}

function search_route(service, x, y) {
    var x1=getQueryString("x");
    var y1=getQueryString("y");

	var pe= new BMap.Point(x,y);
    var ps = new BMap.Point(x1,y1);
    driving.clearResults()
    walking.clearResults()
	service.search(ps, pe);
}

//获取参数
function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)
		return unescape(r[2]);
    }
