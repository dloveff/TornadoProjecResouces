//模式列

function allconsole_recv(){
$.ajax({
		   type:'GET',
		   url: '/recvpattern',
		   success:function(date){
		   $("#console_recv_pattern tr:not(#console_recv_patterntr)").remove();
		   $(date).find("recv-pattern").each(function(){
		            var id = $(this).attr("id");
		            var pattern = $(this).children("pattern").text();
				    var names = $(this).children("name").text();
				    $("#console_recv_pattern").append("<tr><td class='center' data-pattern-pid="+id+">" +pattern+
					"</td><td class='center' data-names-pid="+id+">" +names+ 
					  "</td><td class='center'><a  href='javascript:updateconsole("+id+")'>修改</a>&nbsp;&nbsp;<a  href='javascript:console_recv_patternShow("+id+")'>删除</a></td></tr>");
	
				                   
				   }); 
				
		    	} 
		   });

}


function addconsole(){
$("#addlxrdiv input[name=pattern]").val("");
$("#addlxrdiv input[name=name]").val("");
$("#addconsole_recv").html("");
$("#addlxrdiv").dialog({
			 title : "添加模式",
			 //autoOpen : true,//是否自动弹出
			 time:3000,
			 draggable: true,//是否可拖动
			 height: 250,//默认高度
			 width: 350,//默认宽度
			 maxHeight: 1000,//最大高度
			 maxWidth: 1024,//最大宽度
			 show: "blind", //弹出时的动画效果
		     hide: "explode", //关闭时的动画效果
		     modal:true,//是否是模式对话框
		     buttons:{ //为对话框添加自定义按钮
		    	 "确定添加":function(){
		    		 addPattern();
					
		    	 }	    	 
		     }
		 });

}


function updateconsole(id){
var pattern=$("#console_recv_pattern [data-pattern-pid="+id+"]").text();
var names=$("#console_recv_pattern [data-names-pid="+id+"]").text();
$("#updatepattern").val(pattern);
$("#updatename").val(names);
$("#updatelxrdiv").dialog({
			 title : "修改模式",
			 //autoOpen : true,//是否自动弹出
			 draggable: true,//是否可拖动
			 height: 250,//默认高度
			 width: 350,//默认宽度
			 maxHeight: 1000,//最大高度
			 maxWidth: 1024,//最大宽度
			 show: "blind", //弹出时的动画效果
		     hide: "explode", //关闭时的动画效果
		     modal:true,//是否是模式对话框
		     buttons:{ //为对话框添加自定义按钮
		    	 "确定修改":function(){
		    		updatePattern(id);
		    	 }	    	 
		     }
		 });








}

//添加模式
function addPattern(){

	xmldom = $.parseXML("<recv-pattern/>");
		pattern = $.parseXML("<pattern>" + $("#addlxrdiv input[name=pattern]").val() + "</pattern>").firstChild.cloneNode(true);
		patternname = $.parseXML("<name>" + $("#addlxrdiv input[name=name]").val() + "</name>").firstChild.cloneNode(true);
		xmldom.firstChild.appendChild(pattern);
		xmldom.firstChild.appendChild(patternname);
		pattern = (new XMLSerializer().serializeToString(xmldom));
		 $.ajax({
			    type: 'POST',
			   url: '/recvpattern',
			   data:pattern,
			   success: function(date) {
				  $("#addconsole_recv").html("添加成功");
				   allconsole_recv();
				  $("#addlxrdiv").dialog("close");
			   },error: function(XMLHttpRequest, textStatus, errorThrown) {
                       $("#addconsole_recv").html("添加失败");
                    }

			});
}



//修改模式
function updatePattern(id){
	xmldom = $.parseXML("<recv-pattern/>");
		pattern = $.parseXML("<pattern>" + $("#updatepattern").val() + "</pattern>").firstChild.cloneNode(true);
		patternname = $.parseXML("<name>" + $("#updatename").val() + "</name>").firstChild.cloneNode(true);
		xmldom.firstChild.appendChild(pattern);
		xmldom.firstChild.appendChild(patternname);
		stu = (new XMLSerializer().serializeToString(xmldom));
		 $.ajax({
			    type: 'PUT',
			   url: '/recvpattern/'+id,
			   data:stu,
			   success: function(date) {
				  $("#console_recv").html("修改成功");
				  allconsole_recv();
				  $("#console_recv").html("");
				  $("#updatelxrdiv").dialog("close");
				 
			   },error: function(XMLHttpRequest, textStatus, errorThrown) {
                       $("#console_recv").html("修改失败");
                    }

			});
}
//删除模式
function deletePattern(id){
		 $.ajax({
			    type: 'DELETE',
			   url: '/recvpattern/'+id,
			   async: false,
			   success: function(data) {
				   allconsole_recv();
				  
			   },error: function(XMLHttpRequest, textStatus, errorThrown) {
                       $("#delete").html("删除失败");
                    }

			});
}

