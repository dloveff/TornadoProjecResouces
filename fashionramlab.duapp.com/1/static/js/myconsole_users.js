function allUser(){
$.ajax({
		   type:'GET',
		   url: '/currentuser',
		   success:function(date){
		   $(date).find("user").each(function(){
		            var id = $(this).attr("id");
		            var username = $(this).children("username").text();
				    var fullname = $(this).children("fullname").text();
				    var mobile = $(this).children("mobile").text();
					var email = $(this).children("email").text();
					$("#username").val(username);
					$("#fullname").val(fullname);
					$("#mobile").val(mobile);
					$("#email").val(email);
					$("#mp").val(id);
					$("#fullname1").val(fullname);
					$("#mobile1").val(mobile);
					$("#email1").val(email);
					
					
				                   
				   }); 
				
		    	} 
		   });

}

function logins(){
$("#myconsole").html("");
$(".myconsolelxrdiv").dialog({
			 title : "修改资料",
			 //autoOpen : true,
			 draggable: true,
			 height: 280,
			 width: 350,
			 maxHeight: 1000,
			 maxWidth: 1024,
			 show: "blind", 
		     hide: "explode", 
		     modal:true,
		     buttons:{ 
		    	 "确认修改":function(){
		    		 restPass();
                      $(".myconsolelxrdiv").dialog( "close" );
		    	 },
		    	 "关闭":function(){
		    		 $(".myconsolelxrdiv").dialog("close");
		    	 }		    	 
		     }
		 });

}
function restPass(){
	xmldom = $.parseXML("<user/>");
		fullname = $.parseXML("<fullname>" + $("#fullname1").val() + "</fullname>").firstChild.cloneNode(true);
		mobile = $.parseXML("<mobile>" + $("#mobile1").val() + "</mobile>").firstChild.cloneNode(true);
		email = $.parseXML("<email>" + $("#email1").val() + "</email>").firstChild.cloneNode(true);
		xmldom.firstChild.appendChild(fullname);
		xmldom.firstChild.appendChild(mobile);
		xmldom.firstChild.appendChild(email);
		stu = (new XMLSerializer().serializeToString(xmldom));
		 $.ajax({
			    type: 'PUT',
			   url: '/user',
			   async: false,
			   data:stu,
			   success: function(date) {
				   $("#myconsole").html("修改成功");
				   allUser();
			
			   },error: function(XMLHttpRequest, textStatus, errorThrown) {
                       $("#myconsole").html("修改失败");
                    }

			});
}



function UpdatePassWorld(){
$("#show").html("");
$("#pass").val("");
$(".updateUser").dialog({
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
				     passWords();
					 $(".updateUser").dialog("close");
		    	 },
		    	 "关闭":function(){
		    		 $(".updateUser").dialog("close");//关闭对话框
		    	 }		    	 
		     }
		 });

}
function passWords(){
   var id=$("#mp").val();
	xmldom = $.parseXML("<user/>");
		password = $.parseXML("<password>" + $("#pass").val() + "</password>").firstChild.cloneNode(true);
		xmldom.firstChild.appendChild(password);
		stu = (new XMLSerializer().serializeToString(xmldom));
		 $.ajax({
			    type: 'PUT',
			   url: '/resetpwd/'+id,
			   async: false,
			   data:stu,
			   success: function(data) {
				  $("#show").html("重置成功");
			   },error: function(XMLHttpRequest, textStatus, errorThrown) {
                       $("#show").html("重置失败");
                    }

			});
}