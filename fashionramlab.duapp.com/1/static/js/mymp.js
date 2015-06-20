function add(){
         $("#add_mp_dialog input[name=token]").val(""); 
     $("#add_mp_dialog input[name=name]").val("");
     $("#add_mp_dialog input[name=ghid]").val("");
     $("#add_mp_dialog input[name=appid]").val("");
     $("#add_mp_dialog input[name=secret]").val("");
$("#add_mp_dialog").dialog("open");  
}
function addajax(){
	  xmldom = $.parseXML("<mp/>");
		token = $.parseXML("<token>" + $("#add_mp_dialog input[name=token]").val() + "</token>").firstChild.cloneNode(true);
		mname = $.parseXML("<name>" + $("#add_mp_dialog input[name=name]").val()+ "</name>").firstChild.cloneNode(true);
		ghid =$.parseXML("<ghid>"+$("#add_mp_dialog input[name=ghid]").val()+"</ghid>").firstChild.cloneNode(true);
		appid =$.parseXML("<appid>"+$("#add_mp_dialog input[name=appid]").val()+"</appid>").firstChild.cloneNode(true);
		secret =$.parseXML("<secret>"+$("#add_mp_dialog input[name=secret]").val()+"</secret>").firstChild.cloneNode(true);
	
		xmldom.firstChild.appendChild(token);
		xmldom.firstChild.appendChild(mname);
		xmldom.firstChild.appendChild(ghid);
		xmldom.firstChild.appendChild(appid);
		xmldom.firstChild.appendChild(secret);
		date = (new XMLSerializer().serializeToString(xmldom));
		
    $.ajax({
       type:"POST",
       url:"/mp",
       data:date,
       statusCode:{
       200:function(data){$("#add_mp_dialog").dialog( "close" );$('#find').empty().load('console_mymp.html')},
       401:function(){$("#message").text("添加失败,用户未登录,无权限添加!");},     
       500:function(){$("#message").text("添加错误，请检查输入是否合法!");}
       }  
    });
    
}
function find(){
	$.ajax({//查找
		type:"GET",
		url:"/mymp ",
	  statusCode:{
    200:function(data){
    	$(data).find('mp').each(function(){
				  var mid=$(this).attr("id");
					var token=$(this).find("token").text();
					var mname=$(this).find("name").text();
					var ghid=$(this).find("ghid").text();
					var appid=$(this).find("appid").text();
					var secret=$(this).find("secret").text();
					var enabled=$(this).find("enabled").text();
					$("#body").append( 
					"<tr class="+mid+"><td>"+token+"</td><td>"+mname+"</td>"
					+"<td>"+ghid+"</td><td>"+appid+"</td>"
					+"<td>"+secret+"</td><td>"+enabled+"</td>"
					+"<td><input type='button' value='管理' onclick=manager("+$(this).attr("id")+",'"+token+"')></input>"
					+"<input type='button' value='编辑' onclick=edit("+mid+")></input>"
					+"<input type='button' value='删除' onclick=del('"+mid+"')></input>"
					+"</td></tr>");
			});	
    },
    401:function(){alert("加载数据失败，用户未登录,无权限!");},     
    500:function(){alert("数据加载失败!");}
    }  
	});
}
function manager(mpid, token){
$('#mpid').val(mpid);
$('#token').val(token);
$('#find').empty().load('console_mp.html')
};
function edit(mid){
//从列表中拿到想要的值
  var token=$('tr.'+mid+' td:eq(0)').text();
  var mname=$('tr.'+mid+' td:eq(1)').text();
  var ghid=$('tr.'+mid+' td:eq(2)').text();
  var appid=$('tr.'+mid+' td:eq(3)').text();
  var secret=$('tr.'+mid+' td:eq(4)').text();
  var enabled=$('tr.'+mid+' td:eq(5)').text();

  //给到Dilog
  $("#editmpdiv input[type=hidden]").val(mid);
  $("#etoken").val(token);$("#ename").val(mname);$("#eghid").val(ghid);
  $("#eappid").val(appid);$("#esecret").val(secret);$("#enabled").val(enabled);
  //弹出Dilog
 
   $("#editmpdiv").dialog("open");      
}

function editajax(){
  //生成XML
  xmldom = $.parseXML("<mp/>");
  token = $.parseXML("<token>" + $("#etoken").val() +"</token>").firstChild.cloneNode(true);
  mname = $.parseXML("<name>" + $("#ename").val()+"</name>").firstChild.cloneNode(true);
  ghid =$.parseXML("<ghid>"+$("#eghid").val()+"</ghid>").firstChild.cloneNode(true);
  appid =$.parseXML("<appid>"+$("#eappid").val()+"</appid>").firstChild.cloneNode(true);
  secret =$.parseXML("<secret>"+$("#esecret").val()+"</secret>").firstChild.cloneNode(true);
  enabled =$.parseXML("<enabled>"+$("#enabled").val()+"</enabled>").firstChild.cloneNode(true);

	xmldom.firstChild.appendChild(token);
	xmldom.firstChild.appendChild(mname);
	xmldom.firstChild.appendChild(ghid);
	xmldom.firstChild.appendChild(appid);
	xmldom.firstChild.appendChild(secret);
	xmldom.firstChild.appendChild(enabled);
    
    mid = $("#editmpdiv input[type=hidden]").val();
	date = (new XMLSerializer().serializeToString(xmldom));
	$.ajax({
		type:"PUT",
		url:"/mp/"+mid+"",
		data:date,
		statusCode:{
        200:function(){
            $("#editmpdiv").dialog( "close" );
            $('#find').empty().load('console_mymp.html')
            },
        401:function(){$("#emessage").text("编辑失败,用户未登录,无权限!")},     
        500:function(){$("#emessage").text("编辑失败,请检查输入是否合法!");}
    }  
	});	
}

function del(mid){
xmldom = $.parseXML("<mp/>");
date = (new XMLSerializer().serializeToString(xmldom));
 $.ajax({
    type:"DELETE",
    url:"/mp/"+mid+"",
    data:date,
    statusCode: {
    200:function(){$('#find').empty().load('console_mymp.html')},
    401:function(){alert("删除失败，用户未登录,无权限!");},     
    500:function(){alert("删除数据失败!");}
    }  
 });
}
