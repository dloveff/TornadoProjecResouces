function findList(){
$.ajax({
		   type:'GET',
		   url: '/users',
		   success:function(date){
		   $(date).find("user").each(function(){
		            var id = $(this).attr("id");
		            var username = $(this).children("username").text();
				    var fullname = $(this).children("fullname").text();
				    var mobile = $(this).children("mobile").text();
					var email = $(this).children("email").text();
				    $("#user").append("<tr><td class='center'>" +username+
					"</td><td class='center'>" +fullname+
					 "</td><td class='center'>" +mobile+
					  "</td><td class='center'>" +email+
					  "</td><td class='center'><a class='btn btn-danger' href='javascript:showdialog("+id+");'>重置</a></td></tr>");
	
				                   
				   }); 
				
		    	} 
		   });




}
function showdialog(id){
$("#userest").val("");
$("#userId").html("");
$(".lxrdiv").dialog({
			 title : "重置密码",
			 //autoOpen : true,//是否自动弹出
			 draggable: true,//是否可拖动
			 height: 200,//默认高度
			 width: 350,//默认宽度
			 maxHeight: 1000,//最大高度
			 maxWidth: 1024,//最大宽度
			 show: "blind", //弹出时的动画效果
		     hide: "explode", //关闭时的动画效果
		     modal:true,//是否是模式对话框
		     buttons:{ //为对话框添加自定义按钮
		    	 "确定":function(){
		    		 restPassWorld(id);
					 usercloses();
		    	 },
		    	 "关闭":usercloses=function(){
		    		 $(".lxrdiv").dialog("close");//关闭对话框
		    	 }		    	 
		     }
		 });

}
function restPassWorld(id){
	xmldom = $.parseXML("<user/>");
		password = $.parseXML("<password>" + $("#userest").val() + "</password>").firstChild.cloneNode(true);
		xmldom.firstChild.appendChild(password);
		stu = (new XMLSerializer().serializeToString(xmldom));
		 $.ajax({
			    type: 'PUT',
			   url: '/resetpwd/'+id,
			   data:stu,
			   success: function(data) {
				  $("#userId").html("重置成功");
			   },error: function(XMLHttpRequest, textStatus, errorThrown) {
                       $("#userId").html("重置失败");
                    }

			});
}