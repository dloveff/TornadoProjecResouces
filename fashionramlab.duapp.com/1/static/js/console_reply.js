﻿
//查找全部回复
function findConsole_reply(){
	var id=$("#mpid").val();
	$.ajax({
		   type:'GET',
		   url: '/mpreply/'+id,
		   success:function(date){
			$("#findConsole_reply  tr:not(#tit)").remove();
		    $(date).find("message").each(function(){
		            var id = $(this).attr("id");
		            var pattern = $(this).children("pattern").text();
				    var classname = $(this).children("class").text();
				    var settings = $(this).children("settings").text();
				    $("#findConsole_reply").append("<tr><td>" +pattern+
					"</td><td>" +classname+
					"</td><td>"+ settings+"</td><td><a href='javascript:deleteShow("+id+");'>删除</a></td></tr>");
				   });

		    	}
		   });


}

//输入
function findPut(){
	$.ajax({
		   type:'GET',
		   url: '/recvpattern',
		   success:function(date){
			$("#outReply option").remove();
		   $(date).find("recv-pattern").each(function(){
		            var pattern =$(this).children("pattern").text();
				    var names = $(this).children("name").text();
					var pa = $('<option/>');
					pa.val(pattern);
					pa.text(names);
				    $("#outReply").append(pa);
				   });
				
		    	} 
		   });
}


//输出
function findOut(){
		$.ajax({
		   type:'GET',
		   url: '/replyplugin',
		   success:function(date){
			$("#putReply option").remove();
		   $(date).find("plugin").each(function(){
		            var name = $(this).children("name").text();
				    var na = $(this).children("class").text();
					var pa = $('<option/>');
					pa.val(na);
					pa.text(name);
				    $("#putReply").append(pa);           
				   }); 
				
		    	} 
		   });
}


function show(){
	 $("#settings").val("");
	 $("#dialog-confirm").dialog("open");
	
	
}


function toxml(frmid) {
	frm = $(frmid);
	doc = $.parseXML('<' + frm.attr('name') + '/>');
	$('input[type="hidden"]', frm).each(function(){
		doc.documentElement.setAttribute($(this).attr('name'), $(this).val());
	});
	$('input[type="text"]', frm).each(function() {
		doc.documentElement.appendChild(create_node(this));
	});
	$('select', frm).each(function() {
		doc.documentElement.appendChild(create_node(this));
	});
	
	return (new XMLSerializer().serializeToString(doc));
	
	function create_node(elm) {
		e = doc.createElement($(elm).attr('name'));
		e.appendChild(doc.createCDATASection($(elm).val()));
		return e;
	}
}

function do_submit(frmid, callback) {
	frm = $(frmid);
	var id=$("#mpid").val();
	if(frm.attr('method').toUpperCase() == 'GET') {
		$.ajax({
			type: frm.attr('method'),
			url: frm.attr('action'),
			success: callback
		});
	} else {
	
		$.ajax({
			type: frm.attr('method'),
			url: frm.attr('action'),
			data: toxml(frmid),
			success: function(){
				findConsole_reply();
				
			}
		});
	}
	return false;
}
function mysubmit(frmid) {
	do_submit(frmid, function() {
		return false;
	});
		
}







//删除回复
function deteleConsole_reply(id){
	$.ajax({
		   type:'DELETE',
		   url: '/mpreply/'+id,
		    statusCode: {
			200:function(){findConsole_reply();}
			
			}  
		   });
}
function deleteShow(id){
	$.confirm({
			'title'		: '温馨提示',
			'message'	: '<h5>确认删除？</h5>',
			'buttons'	: {
				'确认'	: {
					'class'	: 'blue',
					'action': function(){
						deteleConsole_reply(id);
					
						
					
					}
				},
				'取消'	: {
					'class'	: 'gray',
					'action': function(){}	
				}
			}
		});
	
	
}
